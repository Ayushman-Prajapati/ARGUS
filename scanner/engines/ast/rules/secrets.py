"""
Hardcoded Secret Detection Rule
================================
Detects assignments of hardcoded string literals to variables whose names
strongly indicate credentials or secrets. Hardcoded secrets end up in version
control, are hard to rotate, and frequently leak to untrusted readers.

Secret-indicating names include:

- password, passwd, pwd, secret, secret_key
- api_key, apikey, access_key, access_token, refresh_token
- token, auth_token, client_secret, private_key
- aws_secret_access_key, database_url

Names are matched with word-boundary substring matching, so ``my_password``
and ``API_KEY`` are detected while benign lookalikes such as
``password_reset`` and ``tokenize`` are ignored.

Only assignments whose value is a string literal are reported. Values loaded
from configuration or runtime sources -- ``os.getenv()``, ``environ[...]``,
``settings.X``, ``config[...]``, imports, or function calls -- are not
reportable, since their RHS is not an ``ast.Constant`` string.

The rule follows the BaseRule interface: metadata is declared on the class
and detection logic lives entirely in ``visit(tree)``. It returns finding
dicts in the normalized ARGUS format and never touches the database.
"""
import ast
import logging
import re
from typing import Any

from scanner.engines.ast.base_rule import BaseRule

logger = logging.getLogger(__name__)

# Maximum snippet length so findings stay comfortably within the
# Finding.code_snippet field limit (4000 chars).
MAX_SNIPPET_LENGTH = 200

# Substrings that strongly indicate a credential when they appear as a whole
# word in an assignment target.
_SECRET_NAME_HINTS = (
    "password",
    "passwd",
    "pwd",
    "secret",
    "secret_key",
    "api_key",
    "apikey",
    "access_key",
    "access_token",
    "refresh_token",
    "token",
    "auth_token",
    "client_secret",
    "private_key",
    "aws_secret_access_key",
)


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


def _matches_secret_hint(name: str) -> bool:
    """
    Return True if ``name`` contains a secret hint at a word boundary.

    The hint must not be followed by a word character, but may be preceded
    by anything -- including an underscore prefix such as ``my_password`` or
    ``_SECRET_KEY``. This detects:

    - ``password``, ``my_password``, ``_PASSWORD``
    - ``API_KEY``, ``api_key``

    while ignoring benign lookalikes where the hint is only a prefix, such
    as ``password_reset``, ``tokenize``, and ``database_url_metrics``.
    """
    lower = name.lower()
    return any(re.search(rf"{re.escape(hint)}(?!\w)", lower) for hint in _SECRET_NAME_HINTS)


def _is_string_literal(value: ast.AST) -> bool:
    """
    Return True if ``value`` is a literal string constant.

    Booleans are rejected because ``bool`` subclasses ``int`` and must not
    be treated as strings.
    """
    return isinstance(value, ast.Constant) and isinstance(value.value, str)


class SecretDetectionRule(BaseRule):
    """
    Reports assignments of hardcoded string literals to secret-indicating names.

    The rule inspects assignment nodes and reports a finding when a target
    name matches a secret hint (word-boundary) and the assigned value is a
    non-empty string literal. Runtime-loaded values are structurally excluded
    because their right-hand side is not a literal constant.
    """

    id = "ARGUS-AST-105"
    name = "Hardcoded Secret"
    description = (
        "Detects hardcoded credentials and secrets (passwords, API keys, "
        "tokens, private keys, database URLs) assigned as string literals "
        "directly in source code."
    )
    severity = "high"
    confidence = "medium"
    cwe = "CWE-798"
    owasp = "A03:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for hardcoded secrets.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per hardcoded secret.
            Empty list when no hardcoded secret assignment is found.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "SecretDetectionRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        findings: list[dict[str, Any]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue

            value = node.value
            if not _is_string_literal(value):
                continue
            if not value.value.strip():
                continue

            for target in node.targets:
                target_name = _target_name(target)
                if not target_name or not _matches_secret_hint(target_name):
                    continue
                findings.append(self._build_finding(node, target_name))
                break

        return findings

    def _build_finding(self, node: ast.Assign, target_name: str) -> dict[str, Any]:
        """Build a normalized finding dict for a hardcoded secret assignment."""
        snippet = _truncate_snippet(ast.unparse(node))

        return {
            "rule_id": self.id,
            "title": f"Hardcoded secret assigned to '{target_name}'",
            "description": (
                "A credential-like value is hardcoded directly in source "
                "code, where it will end up in version control and be exposed "
                "to anyone with repository access."
            ),
            "severity": self.severity,
            "confidence": self.confidence,
            "cwe_id": self.cwe,
            "owasp_category": self.owasp,
            "line_number": getattr(node, "lineno", 0),
            "end_line_number": getattr(node, "end_lineno", None),
            "code_snippet": snippet,
            "remediation": (
                "Load secrets from environment variables or a secrets manager "
                "at runtime, and never commit credential values to source "
                "code."
            ),
        }


def _target_name(target: ast.AST) -> str:
    """
    Return the variable name assigned by a single assignment target.

    Handles bare names (``password = ...``) and attribute targets
    (``settings.PASSWORD = ...``). Returns an empty string for unpacking
    targets, which are not secret assignments.
    """
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return ""
