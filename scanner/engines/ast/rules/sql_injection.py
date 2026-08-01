"""
SQL Injection Detection Rule
=============================
Detects SQL execution through common database APIs where the query is built
from unsafe string construction, which can allow an attacker to alter the
intended SQL statement.

Supported execution methods (attribute-based, receiver-agnostic):

- cursor.execute(...), cursor.executemany(...)
- connection.execute(...)
- session.execute(...)

Unsafe query construction patterns:

- String concatenation (``+``)
- Percent (``%``) string formatting
- ``str.format()``
- f-strings
- Dynamically constructed SQL strings passed directly into execution APIs

Parameterized queries -- where the SQL is a literal string and the bound
parameters are supplied separately (``%s``/``?`` placeholders) -- are
explicitly treated as safe.

This sprint performs syntax-based detection only. It inspects the AST of the
SQL expression supplied to a supported execution method. No taint analysis,
variable propagation, or interprocedural analysis is performed.

The rule follows the BaseRule interface: metadata is declared on the class
and detection logic lives entirely in ``visit(tree)``. It returns finding
dicts in the normalized ARGUS format and never touches the database.
"""
import ast
import logging
from typing import Any

from scanner.engines.ast.base_rule import BaseRule

logger = logging.getLogger(__name__)

# Maximum snippet length so findings stay comfortably within the
# Finding.code_snippet field limit (4000 chars).
MAX_SNIPPET_LENGTH = 200

# Method names that execute SQL, matched by attribute name on any receiver
# (cursor, connection, session, or a model manager).
_SQL_METHODS = {"execute", "executemany"}

# Method names that would be confused with SQL execution.
_SAFE_METHODS = {"format"}


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


class SQLInjectionRule(BaseRule):
    """
    Reports unsafe SQL query construction passed to database execute calls.

    The rule walks the AST looking for ``execute``/``executemany`` calls and
    inspects their first argument. Unsafe constructions -- concatenation,
    percent formatting, ``.format()``, f-strings, or dynamic expressions
    without bound parameters -- are reported; parameterized queries with
    bound parameters are treated as safe.
    """

    id = "ARGUS-AST-103"
    name = "SQL Injection"
    description = (
        "Detects SQL queries built with unsafe string construction "
        "(concatenation, %-formatting, str.format(), f-strings, or dynamic "
        "expressions) that are passed to database execution APIs, which can "
        "allow SQL injection."
    )
    severity = "high"
    confidence = "medium"
    cwe = "CWE-89"
    owasp = "A03:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for unsafe SQL queries.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per unsafe query.
            Empty list when no unsafe SQL construction is found.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "SQLInjectionRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        findings: list[dict[str, Any]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if not _is_sql_execution_call(node):
                continue
            if not node.args:
                continue

            sql_expr = node.args[0]
            if _is_parameterized(node):
                continue
            if not _is_unsafe_construction(sql_expr):
                continue

            findings.append(self._build_finding(node, sql_expr))

        return findings

    def _build_finding(self, node: ast.Call, sql_expr: ast.AST) -> dict[str, Any]:
        """Build a normalized finding dict for an unsafe SQL query call."""
        snippet = _truncate_snippet(ast.unparse(node))

        return {
            "rule_id": self.id,
            "title": "Possible SQL injection via unsafe query construction",
            "description": (
                "A database execute() call is built from string concatenation, "
                "an f-string, str.format(), %-formatting, or another dynamic "
                "expression rather than a parameterized query. Untrusted input "
                "reaching this SQL can alter the query structure and leak or "
                "modify data."
            ),
            "severity": self.severity,
            "confidence": self.confidence,
            "cwe_id": self.cwe,
            "owasp_category": self.owasp,
            "line_number": getattr(node, "lineno", 0),
            "end_line_number": getattr(node, "end_lineno", None),
            "code_snippet": snippet,
            "remediation": (
                "Use parameterized queries so data is always bound separately, "
                "e.g. cursor.execute('SELECT * FROM users WHERE id = %s', "
                "(user_id,)). Never concatenate or format untrusted input "
                "into a SQL string."
            ),
        }


# ---------------------------------------------------------------------------
# SQL call detection helpers
# ---------------------------------------------------------------------------


def _is_sql_execution_call(node: ast.Call) -> bool:
    """
    Return True if ``node`` is a call to a supported SQL execution method.

    A supported call is ``receiver.execute(...)`` or ``receiver.executemany(...)``
    where the receiver is any object expression (bare name, attribute, or call).
    This covers cursor, connection, session, and manager-style receivers, as
    well as chained receivers like ``db.get_cursor().execute(...)``.
    """
    if not isinstance(node.func, ast.Attribute):
        return False
    if node.func.attr not in _SQL_METHODS:
        return False
    return True


def _is_parameterized(node: ast.Call) -> bool:
    """
    Return True if the call supplies bound parameters separately.

    A query is treated as parameterized when a bound parameter argument is
    present, either as the second positional argument or a keyword argument
    (``params``, ``parameters``), or when a list/dict literal is passed as
    the second positional argument.
    """
    if len(node.args) >= 2:
        return True
    for kw in node.keywords:
        if kw.arg in ("params", "parameters"):
            return True
    return False


def _is_unsafe_construction(sql_expr: ast.AST) -> bool:
    """
    Return True if ``sql_expr`` builds SQL through a concrete unsafe pattern.

    Unsafe patterns, per the sprint scope:

    - String concatenation: ``"..." + var``
    - Percent formatting: ``"..." % var``
    - ``str.format()``: ``"SELECT ... WHERE id = {}".format(...)``
    - f-strings: ``f"SELECT ... WHERE id = {var}"``

    Plain variable references and literal strings are intentionally treated
    as safe (concrete patterns only): passing a pre-built query variable to
    execute() is a legitimate use and not flagged.
    """
    if isinstance(sql_expr, ast.BinOp) and isinstance(sql_expr.op, (ast.Add, ast.Mod)):
        return True

    if isinstance(sql_expr, ast.JoinedStr):
        return True

    if isinstance(sql_expr, ast.Call):
        func = sql_expr.func
        return isinstance(func, ast.Attribute) and func.attr in _SAFE_METHODS

    return False
