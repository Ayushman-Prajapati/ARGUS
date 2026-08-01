"""
Command Injection Detection Rule
=================================
Detects calls to command execution APIs in the ``os`` and ``subprocess``
modules:

- os.system(), os.popen()
- subprocess.run(), subprocess.Popen(), subprocess.call(),
  subprocess.check_call(), subprocess.check_output()

These APIs can execute external commands. When the command string is built
from untrusted input (or ``shell=True`` is used), an attacker can inject
arbitrary shell commands.

This sprint detects API usage only. No taint analysis, data-flow analysis,
or argument validation is performed -- a call to a supported API is reported
regardless of its arguments.

Calls are resolved to their fully-qualified name using AST-based import
analysis, so aliased imports are detected too:

    import subprocess as sp
    sp.run(cmd)            # resolved to subprocess.run

    from os import system
    system(cmd)            # resolved to os.system

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

# Fully-qualified command execution APIs and their metadata so each call
# carries the right title, description, and remediation without branching.
_COMMAND_APIS: dict[str, dict[str, str]] = {
    "os.system": {
        "title": "Shell command execution via os.system()",
        "description": (
            "os.system() passes a command string to the system shell. If any "
            "part of that string is attacker-influenced, the attacker can "
            "execute arbitrary shell commands on the host."
        ),
        "remediation": (
            "Prefer subprocess.run([...], shell=False) with the command and "
            "its arguments passed as a list. Never pass an untrusted string "
            "to a shell."
        ),
    },
    "os.popen": {
        "title": "Shell command execution via os.popen()",
        "description": (
            "os.popen() opens a pipe to a shell and runs the given command "
            "string. Attacker-controlled input reaching the string can be "
            "interpreted as shell metacharacters, enabling arbitrary command "
            "execution."
        ),
        "remediation": (
            "Replace os.popen() with subprocess.run([...], shell=False, "
            "capture_output=True) or subprocess.Popen with an argument list."
        ),
    },
    "subprocess.run": {
        "title": "Subprocess execution via subprocess.run()",
        "description": (
            "subprocess.run() executes an external program. When invoked with "
            "shell=True or a command string assembled from untrusted input, "
            "it can lead to OS command injection."
        ),
        "remediation": (
            "Pass the command as a list of arguments and keep shell=False "
            "(the default). Never concatenate user input into a command "
            "string."
        ),
    },
    "subprocess.Popen": {
        "title": "Subprocess execution via subprocess.Popen()",
        "description": (
            "subprocess.Popen() starts an external program. Used with "
            "shell=True or an attacker-influenced command string, it can "
            "execute arbitrary shell commands."
        ),
        "remediation": (
            "Invoke subprocess.Popen with a list of arguments and shell=False. "
            "Avoid passing a command string built from untrusted input."
        ),
    },
    "subprocess.call": {
        "title": "Subprocess execution via subprocess.call()",
        "description": (
            "subprocess.call() runs an external command and waits for it to "
            "finish. shell=True or an untrusted command string enables shell "
            "command injection."
        ),
        "remediation": (
            "Use subprocess.run([...], shell=False) or subprocess.Popen with "
            "an argument list instead of a shell string."
        ),
    },
    "subprocess.check_call": {
        "title": "Subprocess execution via subprocess.check_call()",
        "description": (
            "subprocess.check_call() runs a command and raises on a non-zero "
            "exit code. When invoked with shell=True or a command string "
            "built from untrusted input, it can execute arbitrary shell "
            "commands."
        ),
        "remediation": (
            "Pass the command as a list and use shell=False. Never build the "
            "command string from untrusted input."
        ),
    },
    "subprocess.check_output": {
        "title": "Subprocess execution via subprocess.check_output()",
        "description": (
            "subprocess.check_output() runs a command and captures its "
            "output. shell=True or an attacker-influenced command string "
            "exposes a shell command injection vector."
        ),
        "remediation": (
            "Invoke subprocess.check_output with a list of arguments and "
            "shell=False, and keep untrusted input out of the command."
        ),
    },
}


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


class CommandInjectionRule(BaseRule):
    """
    Reports calls to the supported ``os``/``subprocess`` command APIs.

    The rule builds a module-wide import map from the AST, then reports any
    call whose fully-qualified name matches a known command execution API.
    Import aliases are resolved so ``import subprocess as sp`` and
    ``from subprocess import run`` are detected alongside the literal
    dotted forms.
    """

    id = "ARGUS-AST-102"
    name = "Command Injection"
    description = (
        "Detects calls to command execution APIs in the os and subprocess "
        "modules (os.system, os.popen, subprocess.run, subprocess.Popen, "
        "subprocess.call, subprocess.check_call, subprocess.check_output), "
        "which can lead to OS command injection when invoked on untrusted "
        "input."
    )
    severity = "high"
    confidence = "medium"
    cwe = "CWE-78"
    owasp = "A03:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for command execution calls.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per detected call.
            Empty list when no supported API is called.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "CommandInjectionRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        import_map = _build_import_map(tree)
        findings: list[dict[str, Any]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            dotted_name = _resolve_call_name(node.func, import_map)
            if dotted_name not in _COMMAND_APIS:
                continue

            findings.append(self._build_finding(node, dotted_name))

        return findings

    def _build_finding(self, node: ast.Call, dotted_name: str) -> dict[str, Any]:
        """Build a normalized finding dict for a command API call node."""
        meta = _COMMAND_APIS[dotted_name]
        snippet = _truncate_snippet(ast.unparse(node))

        return {
            "rule_id": self.id,
            "title": meta["title"],
            "description": meta["description"],
            "severity": self.severity,
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

    Handles ``import os``, ``import os as o``, ``from os import system``,
    and ``from subprocess import run as sub_run``.
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

    - ``os.system`` -> ``os.system``
    - ``sp.run`` (import subprocess as sp) -> ``subprocess.run``
    - ``run`` (from subprocess import run) -> ``subprocess.run``
    - Unimported bare names and non-call expressions resolve to a name that
      will not match any command API.
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
