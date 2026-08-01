"""
Dangerous Function Detection Rule
==================================
Detects direct calls to Python's dangerous built-in functions:
eval(), exec(), and compile().

These built-ins can execute arbitrary Python code supplied by the caller,
making them a primary vector for code injection when invoked on untrusted
input. Only direct calls (``eval(...)``) are reported; method attributes
(``obj.eval()``) and references to shadowed names are ignored to keep the
rule focused and low-noise.

The rule follows the BaseRule interface: metadata is declared on the class
and detection logic lives entirely in ``visit(tree)``. It returns finding
dicts in the normalized ARGUS format and never touches the database.

Shadow detection
----------------
A call is only reported when the name resolves to the Python built-in.
If the same module redefines ``eval``/``exec``/``compile`` -- as a function,
variable, parameter, import, or loop target -- the rule treats those calls as
calls to the user's own binding and skips them. Resolution is scope-aware:
a name bound inside a function shadows only inside that function (and its
nested scopes), while module-level bindings shadow the whole module.
"""
import ast
import logging
from typing import Any

from scanner.engines.ast.base_rule import BaseRule

logger = logging.getLogger(__name__)

# Maximum snippet length so findings stay comfortably within the
# Finding.code_snippet field limit (4000 chars).
MAX_SNIPPET_LENGTH = 200

# Per-function metadata so each detected built-in carries the right
# description, CWE, and remediation without per-call branching.
_FUNCTION_METADATA: dict[str, dict[str, str]] = {
    "eval": {
        "description": (
            "eval() executes the passed string as Python code. When the input "
            "is not fully trusted, an attacker can inject arbitrary code into "
            "the process, leading to remote code execution."
        ),
        "cwe_id": "CWE-95",
        "remediation": (
            "Avoid eval() entirely. If dynamic behavior is truly required, "
            "use a safe alternative such as ast.literal_eval(), and never "
            "pass untrusted input to an interpreter."
        ),
    },
    "exec": {
        "description": (
            "exec() compiles and runs the passed string as Python code. Any "
            "untrusted content reaching exec() can execute arbitrary "
            "statements in the current scope."
        ),
        "cwe_id": "CWE-95",
        "remediation": (
            "Avoid exec() entirely. Refactor the logic to use explicit data "
            "structures, and never build or run Python source from untrusted "
            "input."
        ),
    },
    "compile": {
        "description": (
            "compile() compiles source text into a code object that can later "
            "be executed. Compiling untrusted source enables arbitrary code "
            "execution in the surrounding application."
        ),
        "cwe_id": "CWE-94",
        "remediation": (
            "Never compile source that is not fully trusted. If code "
            "generation is unavoidable, restrict the source to a safe, "
            "verifiable subset."
        ),
    },
}

# Scope nodes whose namespace participates in built-in name resolution.
_SCOPE_NODES = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


class DangerousFunctionRule(BaseRule):
    """
    Reports direct calls to eval(), exec(), and compile().

    The rule walks the AST looking for Call nodes whose function is a bare
    ``ast.Name`` matching a dangerous built-in. Only the call expression is
    captured (e.g. ``eval(user_input)``), never surrounding statements, and
    calls shadowed by a user binding are not reported.
    """

    id = "ARGUS-AST-101"
    name = "Dangerous Function"
    description = (
        "Detects direct calls to the dangerous Python built-ins eval(), "
        "exec(), and compile(), which can execute arbitrary code when given "
        "untrusted input."
    )
    severity = "high"
    confidence = "medium"
    cwe = "CWE-95"
    owasp = "A03:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for dangerous built-ins.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per detected call.
            Empty list when the code is safe.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "DangerousFunctionRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        parent_map, bound_by_scope = _build_scope_map(tree)
        findings: list[dict[str, Any]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            # Only direct calls to a bare name count; attribute calls such as
            # obj.eval() are unrelated, as are variable references.
            if not isinstance(node.func, ast.Name):
                continue
            func_name = node.func.id
            if func_name not in _FUNCTION_METADATA:
                continue
            if _is_name_shadowed(node, func_name, parent_map, bound_by_scope):
                continue

            findings.append(self._build_finding(node, func_name))

        return findings

    def _build_finding(self, node: ast.Call, func_name: str) -> dict[str, Any]:
        """Build a normalized finding dict for a dangerous call node."""
        meta = _FUNCTION_METADATA[func_name]
        title = f"Use of dangerous function: {func_name}()"
        snippet = _truncate_snippet(ast.unparse(node))

        return {
            "rule_id": self.id,
            "title": title,
            "description": meta["description"],
            "severity": self.severity,
            "confidence": self.confidence,
            "cwe_id": meta["cwe_id"],
            "owasp_category": self.owasp,
            "line_number": getattr(node, "lineno", 0),
            "end_line_number": getattr(node, "end_lineno", None),
            "code_snippet": snippet,
            "remediation": meta["remediation"],
        }


# ---------------------------------------------------------------------------
# Scope tracking helpers
# ---------------------------------------------------------------------------


def _build_scope_map(tree: ast.AST) -> tuple[dict, dict]:
    """
    Build parent links and the names bound in each scope.

    Returns ``(parent_map, bound_by_scope)`` where parent_map maps each node
    to its parent and bound_by_scope maps scope nodes (Module, FunctionDef,
    ClassDef) to the set of names bound directly in that scope.
    """
    parent_map: dict[Any, Any] = {}
    bound_by_scope: dict[Any, set[str]] = {}

    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent_map[child] = node
        if isinstance(node, _SCOPE_NODES):
            bound_by_scope[node] = _scope_bound_names(node)

    return parent_map, bound_by_scope


def _scope_bound_names(scope: Any) -> set[str]:
    """Return the names bound directly inside a scope (not nested scopes)."""
    names = _param_names(scope) if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)) else set()
    for node in _iter_scope_level_nodes(scope):
        names.update(_binding_names(node))
    return names


def _iter_scope_level_nodes(scope: Any):
    """Yield nodes in a scope's body, never descending into nested scopes."""
    for child in ast.iter_child_nodes(scope):
        yield from _iter_without_nested_scopes(child)


def _iter_without_nested_scopes(node: Any):
    """Yield ``node`` and its descendants, stopping at nested function/class scopes."""
    yield node
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return
    for child in ast.iter_child_nodes(node):
        yield from _iter_without_nested_scopes(child)


def _param_names(scope: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return the names of a function's parameters."""
    names = {arg.arg for arg in scope.args.posonlyargs + scope.args.args + scope.args.kwonlyargs}
    if scope.args.vararg:
        names.add(scope.args.vararg.arg)
    if scope.args.kwarg:
        names.add(scope.args.kwarg.arg)
    return names


def _binding_names(node: Any) -> set[str]:
    """Return the names bound by a single statement/expression node."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, ast.Assign):
        return {name for target in node.targets for name in _target_names(target)}
    if isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.For, ast.NamedExpr)):
        return _target_names(node.target)
    if isinstance(node, ast.Import):
        return {alias.asname or alias.name.split(".")[0] for alias in node.names}
    if isinstance(node, ast.ImportFrom):
        return {alias.asname or alias.name for alias in node.names}
    if isinstance(node, ast.With):
        names: set[str] = set()
        for item in node.items:
            if item.optional_vars is not None:
                names.update(_target_names(item.optional_vars))
        return names
    if isinstance(node, ast.ExceptHandler):
        return {node.name} if node.name else set()
    if isinstance(node, ast.comprehension):
        return _target_names(node.target)
    return set()


def _target_names(target: Any) -> set[str]:
    """Return the names assigned by a simple or starred/tuple target."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        names: set[str] = set()
        for element in target.elts:
            names.update(_target_names(element))
        return names
    if isinstance(target, ast.Starred):
        return _target_names(target.value)
    return set()


def _is_name_shadowed(
    call_node: ast.AST,
    name: str,
    parent_map: dict,
    bound_by_scope: dict,
) -> bool:
    """
    Return True if ``name`` does not resolve to a built-in at ``call_node``.

    Resolution walks the lexical scopes from the call site outward. Function
    locals are consulted innermost-first; class namespaces are consulted only
    for code written directly in the class body (methods resolve past their
    containing class, matching Python semantics).
    """
    in_function = False
    current: Any = call_node
    while current is not None:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
            in_function = True
        elif isinstance(current, ast.ClassDef) and in_function:
            # Methods and nested functions skip the containing class namespace.
            current = parent_map.get(current)
            continue

        if name in bound_by_scope.get(current, ()):
            return True

        current = parent_map.get(current)

    return False
