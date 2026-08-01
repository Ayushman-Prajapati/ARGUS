"""
Unsafe Deserialization Detection Rule
======================================
Detects calls to deserialization APIs that are unsafe by default. These
libraries can reconstruct arbitrary objects -- and in some cases execute
arbitrary code -- from untrusted serialized data.

Unsafe APIs by module:

- pickle.load(), pickle.loads()
- cPickle.load(), cPickle.loads()
- dill.load(), dill.loads()
- marshal.load(), marshal.loads()
- shelve.open()
- yaml.load()

``yaml.safe_load()`` and ``yaml.load()`` calls that explicitly pass a safe
``Loader`` are explicitly safe and are not reported.

Calls are resolved to their fully-qualified name using the same AST-based
import analysis as the Command Injection rule, so aliased imports are
detected too:

    import pickle as p
    p.loads(data)          # resolved to pickle.loads

    from yaml import load
    load(stream)           # resolved to yaml.load

This sprint detects unsafe API usage only. No taint analysis, trust-boundary
analysis, or data-flow analysis is performed.

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

# Fully-qualified unsafe deserialization APIs and their metadata.
_DESERIALIZATION_APIS: dict[str, dict[str, str]] = {
    "pickle.load": {
        "title": "Unsafe deserialization via pickle.load()",
        "severity": "critical",
        "remediation": (
            "Never unpickle untrusted data. Use a safer format such as JSON, "
            "or a library designed for untrusted input. If pickle is required, "
            "only load data from a trusted, authenticated source."
        ),
    },
    "pickle.loads": {
        "title": "Unsafe deserialization via pickle.loads()",
        "severity": "critical",
        "remediation": (
            "Never unpickle untrusted data. Use a safer format such as JSON, "
            "or a library designed for untrusted input. If pickle is required, "
            "only load data from a trusted, authenticated source."
        ),
    },
    "cPickle.load": {
        "title": "Unsafe deserialization via cPickle.load()",
        "severity": "critical",
        "remediation": (
            "cPickle is a C implementation of pickle with the same risks. "
            "Never deserialize untrusted data; prefer a safe format like JSON."
        ),
    },
    "cPickle.loads": {
        "title": "Unsafe deserialization via cPickle.loads()",
        "severity": "critical",
        "remediation": (
            "cPickle is a C implementation of pickle with the same risks. "
            "Never deserialize untrusted data; prefer a safe format like JSON."
        ),
    },
    "dill.load": {
        "title": "Unsafe deserialization via dill.load()",
        "severity": "critical",
        "remediation": (
            "dill extends pickle and can reconstruct full Python objects and "
            "code, making it even more dangerous on untrusted data. Prefer a "
            "safe serialization format."
        ),
    },
    "dill.loads": {
        "title": "Unsafe deserialization via dill.loads()",
        "severity": "critical",
        "remediation": (
            "dill extends pickle and can reconstruct full Python objects and "
            "code, making it even more dangerous on untrusted data. Prefer a "
            "safe serialization format."
        ),
    },
    "marshal.load": {
        "title": "Unsafe deserialization via marshal.load()",
        "severity": "high",
        "remediation": (
            "marshal data is not a safe serialization format and can reference "
            "arbitrary code objects. Use a safe format such as JSON for "
            "untrusted input."
        ),
    },
    "marshal.loads": {
        "title": "Unsafe deserialization via marshal.loads()",
        "severity": "high",
        "remediation": (
            "marshal data is not a safe serialization format and can reference "
            "arbitrary code objects. Use a safe format such as JSON for "
            "untrusted input."
        ),
    },
    "shelve.open": {
        "title": "Unsafe deserialization via shelve.open()",
        "severity": "high",
        "remediation": (
            "shelve persists objects using pickle, so reading an attacker-"
            "controlled shelf can execute arbitrary code. Only open shelves "
            "you fully control."
        ),
    },
    "yaml.load": {
        "title": "Unsafe deserialization via yaml.load()",
        "severity": "high",
        "remediation": (
            "yaml.load() constructs arbitrary Python objects from YAML unless "
            "a safe Loader is supplied. Use yaml.safe_load() instead."
        ),
    },
}

# Loader names that make yaml.load() explicitly safe.
# Only officially supported PyYAML safe loaders are recognized.
_SAFE_YAML_LOADERS = {"SafeLoader", "CSafeLoader"}


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


class DeserializationRule(BaseRule):
    """
    Reports calls to deserialization APIs that are unsafe by default.

    The rule builds a module-wide import map from the AST, then reports any
    call whose fully-qualified name matches a known unsafe deserialization
    API. Import aliases are resolved so ``import pickle as p`` and
    ``from pickle import loads`` are detected alongside the literal dotted
    forms. ``yaml.safe_load`` and ``yaml.load`` with an explicit safe
    ``Loader`` are not reported.
    """

    id = "ARGUS-AST-104"
    name = "Unsafe Deserialization"
    description = (
        "Detects calls to deserialization APIs (pickle, cPickle, dill, "
        "marshal, shelve, yaml) that are unsafe by default, which can execute "
        "arbitrary code when deserializing untrusted data."
    )
    severity = "high"
    confidence = "medium"
    cwe = "CWE-502"
    owasp = "A03:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for unsafe deserialization calls.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per detected call.
            Empty list when no unsafe API is called.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "DeserializationRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        import_map = _build_import_map(tree)
        findings: list[dict[str, Any]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            dotted_name = _resolve_call_name(node.func, import_map)
            if dotted_name not in _DESERIALIZATION_APIS:
                continue

            if dotted_name == "yaml.load" and _has_safe_loader(node):
                continue

            findings.append(self._build_finding(node, dotted_name))

        return findings

    def _build_finding(self, node: ast.Call, dotted_name: str) -> dict[str, Any]:
        """Build a normalized finding dict for an unsafe deserialization call."""
        meta = _DESERIALIZATION_APIS[dotted_name]
        snippet = _truncate_snippet(ast.unparse(node))

        return {
            "rule_id": self.id,
            "title": meta["title"],
            "description": (
                f"{dotted_name}() can execute arbitrary code when "
                "deserializing attacker-controlled data. Deserializing "
                "untrusted input with this API is an unsafe-by-default "
                "operation."
            ),
            "severity": meta["severity"],
            "confidence": self.confidence,
            "cwe_id": self.cwe,
            "owasp_category": self.owasp,
            "line_number": getattr(node, "lineno", 0),
            "end_line_number": getattr(node, "end_lineno", None),
            "code_snippet": snippet,
            "remediation": meta["remediation"],
        }


# ---------------------------------------------------------------------------
# Import-aware call resolution helpers
# ---------------------------------------------------------------------------


def _build_import_map(tree: ast.AST) -> dict[str, str]:
    """
    Map every local name to the fully-qualified name it refers to.

    Handles ``import pickle``, ``import pickle as p``, ``from pickle import
    loads``, and ``from pickle import loads as p_loads``.
    """
    import_map: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                import_map[local] = alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                local = alias.asname or alias.name
                import_map[local] = f"{node.module}.{alias.name}"

    return import_map


def _resolve_call_name(func: Any, import_map: dict[str, str]) -> str:
    """
    Resolve a call's function expression to its fully-qualified dotted name.

    - ``pickle.load`` -> ``pickle.load``
    - ``p.loads`` (import pickle as p) -> ``pickle.loads``
    - ``loads`` (from pickle import loads) -> ``pickle.loads``
    - Unimported bare names and non-call expressions resolve to a name that
      will not match any unsafe deserialization API.
    """
    if isinstance(func, ast.Name):
        return import_map.get(func.id, func.id)
    if isinstance(func, ast.Attribute):
        parts = []
        while isinstance(func, ast.Attribute):
            parts.append(func.attr)
            func = func.value
        if isinstance(func, ast.Name):
            parts.append(import_map.get(func.id, func.id))
            return ".".join(reversed(parts))
    return ""


def _has_safe_loader(node: ast.Call) -> bool:
    """
    Return True if a yaml.load() call explicitly passes a safe Loader.

    A safe Loader may be supplied as the ``Loader`` keyword argument or as a
    positional ``Loader`` argument.
    """
    for kw in node.keywords:
        if kw.arg == "Loader" and _is_safe_loader_value(kw.value):
            return True

    for arg in node.args:
        if _is_safe_loader_value(arg):
            return True

    return False


def _is_safe_loader_value(value: Any) -> bool:
    """Return True if a Loader value names an explicitly safe loader."""
    if isinstance(value, ast.Name):
        return value.id in _SAFE_YAML_LOADERS
    if isinstance(value, ast.Attribute):
        return value.attr in _SAFE_YAML_LOADERS
    return False
