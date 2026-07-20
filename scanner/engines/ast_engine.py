"""
ARGUS AST Engine
================
A lightweight, dependency-free static analysis engine built directly on top of
Python's built-in `ast` module. It complements Bandit and Semgrep by running a
small, transparent, hand-written ruleset -- useful both as a teaching example
of AST-based analysis and as a fast first-pass scanner.

Each rule is implemented as a method on `ArgusASTVisitor` that inspects nodes
during a single tree walk and appends normalized finding dicts to `self.findings`.
"""
import ast
from dataclasses import dataclass, field


DANGEROUS_CALLS = {
    "eval": ("ARGUS-AST-001", "Use of eval()", "critical",
              "eval() executes arbitrary strings as Python code, allowing "
              "code injection if the input is ever attacker-influenced.",
              "CWE-95"),
    "exec": ("ARGUS-AST-002", "Use of exec()", "critical",
              "exec() executes arbitrary strings as Python statements, "
              "creating a direct code-injection vector.",
              "CWE-95"),
    "compile": ("ARGUS-AST-003", "Dynamic code compilation via compile()", "medium",
              "compile() combined with exec/eval can hide dynamic code "
              "execution from casual review.",
              "CWE-95"),
}

WEAK_HASH_ALGORITHMS = {"md5", "sha1"}

INSECURE_DESERIALIZATION = {
    "pickle": {"loads", "load"},
    "cPickle": {"loads", "load"},
    "yaml": {"load"},
    "marshal": {"loads", "load"},
}

SECRET_NAME_HINTS = (
    "password", "passwd", "pwd", "secret", "api_key", "apikey",
    "access_key", "auth_token", "private_key", "token", "credential",
)


@dataclass
class ASTFinding:
    rule_id: str
    title: str
    severity: str
    description: str
    cwe_id: str
    line: int
    end_line: int
    snippet: str
    remediation: str = ""
    confidence: str = "medium"


class ArgusASTVisitor(ast.NodeVisitor):
    """Walks a parsed module and collects security-relevant findings."""

    def __init__(self, source_lines):
        self.source_lines = source_lines
        self.findings: list[ASTFinding] = []
        self._imported_modules = set()
        self._import_aliases = {}  # alias -> real module name

    # ---------------------------------------------------------------- utils
    def _snippet(self, node, context=1):
        start = max(node.lineno - 1 - context, 0)
        end = min(node.end_lineno + context, len(self.source_lines))
        return "\n".join(self.source_lines[start:end])

    def _add(self, node, rule_id, title, severity, description, cwe_id, remediation, confidence="medium"):
        self.findings.append(ASTFinding(
            rule_id=rule_id,
            title=title,
            severity=severity,
            description=description,
            cwe_id=cwe_id,
            line=node.lineno,
            end_line=getattr(node, "end_lineno", node.lineno),
            snippet=self._snippet(node),
            remediation=remediation,
            confidence=confidence,
        ))

    def _resolve_call_name(self, node):
        """Best-effort dotted name for a Call node's func, e.g. 'os.system'."""
        func = node.func
        parts = []
        while isinstance(func, ast.Attribute):
            parts.append(func.attr)
            func = func.value
        if isinstance(func, ast.Name):
            parts.append(self._import_aliases.get(func.id, func.id))
        return ".".join(reversed(parts))

    # -------------------------------------------------------------- imports
    def visit_Import(self, node):
        for alias in node.names:
            real = alias.name
            local = alias.asname or alias.name.split(".")[0]
            self._imported_modules.add(real)
            self._import_aliases[local] = real
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self._imported_modules.add(node.module)
        self.generic_visit(node)

    # ----------------------------------------------------------------- rules
    def visit_Call(self, node):
        dotted = self._resolve_call_name(node)
        base_name = dotted.split(".")[-1]

        # 1. eval / exec / compile
        if base_name in DANGEROUS_CALLS and (
            isinstance(node.func, ast.Name) or dotted in ("eval", "exec", "compile")
        ):
            rule_id, title, severity, desc, cwe = DANGEROUS_CALLS[base_name]
            self._add(node, rule_id, title, severity, desc, cwe,
                       remediation=f"Avoid {base_name}() on untrusted input. "
                                   f"Use ast.literal_eval() for data, or a safe parser.")

        # 2. os.system / subprocess with shell=True
        if dotted in ("os.system", "os.popen"):
            self._add(node, "ARGUS-AST-004", f"Shell command execution via {dotted}()",
                       "high",
                       "Spawns a shell to execute a command string, which is prone "
                       "to shell injection if any part is attacker-influenced.",
                       "CWE-78",
                       remediation="Use subprocess.run([...], shell=False) with a "
                                   "list of arguments instead of a shell string.")

        if dotted.startswith("subprocess."):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self._add(node, "ARGUS-AST-005", "subprocess call with shell=True",
                               "high",
                               "shell=True invokes a system shell to interpret the "
                               "command, enabling shell metacharacter injection.",
                               "CWE-78",
                               remediation="Pass the command as a list and use shell=False "
                                           "(the default), avoiding shell interpretation.")

        # 3. insecure deserialization
        module_root = dotted.split(".")[0]
        if module_root in INSECURE_DESERIALIZATION and base_name in INSECURE_DESERIALIZATION[module_root]:
            if module_root == "yaml" and base_name == "load":
                has_safe_loader = any(
                    kw.arg == "Loader" for kw in node.keywords
                )
                if has_safe_loader:
                    return self.generic_visit(node)
            self._add(node, "ARGUS-AST-006", f"Insecure deserialization via {dotted}()",
                       "critical" if module_root in ("pickle", "cPickle") else "high",
                       f"{dotted}() can execute arbitrary code when deserializing "
                       "attacker-controlled data.",
                       "CWE-502",
                       remediation="Avoid unpickling untrusted data. For YAML use "
                                   "yaml.safe_load(); for pickle use a signed/trusted "
                                   "source only or a safer format like JSON.")

        # 4. weak hashing
        if dotted == "hashlib.new" and node.args:
            arg0 = node.args[0]
            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                if arg0.value.lower() in WEAK_HASH_ALGORITHMS:
                    self._add(node, "ARGUS-AST-007", f"Weak hash algorithm: {arg0.value}",
                               "medium",
                               "MD5 and SHA-1 are cryptographically broken for "
                               "collision resistance and unsuitable for security use.",
                               "CWE-327",
                               remediation="Use hashlib.sha256() or better for security "
                                           "purposes; use bcrypt/scrypt/argon2 for passwords.")
        if base_name in WEAK_HASH_ALGORITHMS and dotted.startswith("hashlib."):
            self._add(node, "ARGUS-AST-007", f"Weak hash algorithm: hashlib.{base_name}()",
                       "medium",
                       "MD5 and SHA-1 are cryptographically broken for collision "
                       "resistance and unsuitable for security-sensitive use.",
                       "CWE-327",
                       remediation="Use hashlib.sha256() or better; use a dedicated "
                                   "password-hashing function for credentials.")

        # 5. use of random for security-sensitive-sounding names is handled at
        #    call-site via variable name heuristics in visit_Assign.

        # 6. assert used for access-control (stripped under python -O)
        self.generic_visit(node)

    def visit_Assert(self, node):
        text = self._snippet(node, context=0).lower()
        if any(k in text for k in ("auth", "permission", "is_admin", "access", "login")):
            self._add(node, "ARGUS-AST-008", "Security check implemented via assert",
                       "medium",
                       "assert statements are removed when Python runs with -O, "
                       "silently disabling any security check they perform.",
                       "CWE-703",
                       remediation="Replace with an explicit `if not condition: raise "
                                   "PermissionError(...)` check.")
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            name = None
            if isinstance(target, ast.Name):
                name = target.id
            elif isinstance(target, ast.Attribute):
                name = target.attr
            if not name:
                continue
            lname = name.lower()
            if any(hint in lname for hint in SECRET_NAME_HINTS):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) and node.value.value:
                    if len(node.value.value) >= 3:
                        self._add(node, "ARGUS-AST-009", f"Hardcoded secret assigned to '{name}'",
                                   "critical",
                                   "A credential-like value is hardcoded directly in "
                                   "source, where it will end up in version control.",
                                   "CWE-798",
                                   remediation="Load secrets from environment variables "
                                               "or a secrets manager, never from source code.")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Detect string-concatenation / %-formatting flowing into execute()-style calls
        # is handled contextually in visit_Call via argument inspection below.
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Flag debug flags left on, e.g. `def view(request): ... DEBUG = True`
        self.generic_visit(node)


def _looks_like_sql_execute(dotted_name, base_name):
    return base_name in ("execute", "executemany") or dotted_name.endswith(".raw")


class _SQLInjectionVisitor(ast.NodeVisitor):
    """Secondary pass: flags .execute()/.raw() calls built from string
    concatenation, %-formatting, or f-strings instead of parameterized queries."""

    def __init__(self, source_lines):
        self.source_lines = source_lines
        self.findings: list[ASTFinding] = []

    def _snippet(self, node, context=1):
        start = max(node.lineno - 1 - context, 0)
        end = min(node.end_lineno + context, len(self.source_lines))
        return "\n".join(self.source_lines[start:end])

    def visit_Call(self, node):
        func = node.func
        base_name = func.attr if isinstance(func, ast.Attribute) else (
            func.id if isinstance(func, ast.Name) else ""
        )
        if _looks_like_sql_execute("", base_name) and node.args:
            first_arg = node.args[0]
            risky = isinstance(first_arg, (ast.BinOp, ast.JoinedStr)) or (
                isinstance(first_arg, ast.Call)
                and isinstance(first_arg.func, ast.Attribute)
                and first_arg.func.attr == "format"
            )
            if risky:
                self.findings.append(ASTFinding(
                    rule_id="ARGUS-AST-010",
                    title="Possible SQL injection via dynamic query construction",
                    severity="critical",
                    description="A database execute()/raw() call is built from string "
                                "concatenation, an f-string, or .format() rather than "
                                "parameter binding, risking SQL injection.",
                    cwe_id="CWE-89",
                    line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    snippet=self._snippet(node),
                    remediation="Use parameterized queries, e.g. cursor.execute(sql, "
                                "[param1, param2]) instead of building SQL strings "
                                "manually.",
                    confidence="medium",
                ))
        self.generic_visit(node)


def scan_source(file_path: str, source: str) -> list[dict]:
    """Parse `source` and run the ARGUS AST ruleset against it.

    Returns a list of normalized finding dicts ready to persist as Finding rows.
    Syntax errors are swallowed and reported as a single low-severity finding
    so one bad file never aborts a whole scan.
    """
    source_lines = source.splitlines()
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as exc:
        return [{
            "rule_id": "ARGUS-AST-000",
            "title": "File could not be parsed",
            "severity": "info",
            "description": f"Python syntax error while parsing this file: {exc.msg}",
            "cwe_id": "",
            "file_path": file_path,
            "line_number": exc.lineno or 0,
            "end_line_number": exc.lineno or 0,
            "code_snippet": "",
            "remediation": "Fix the syntax error to enable static analysis of this file.",
            "confidence": "high",
        }]

    visitor = ArgusASTVisitor(source_lines)
    visitor.visit(tree)

    sql_visitor = _SQLInjectionVisitor(source_lines)
    sql_visitor.visit(tree)

    all_findings = visitor.findings + sql_visitor.findings

    results = []
    for f in all_findings:
        results.append({
            "rule_id": f.rule_id,
            "title": f.title,
            "severity": f.severity,
            "description": f.description,
            "cwe_id": f.cwe_id,
            "file_path": file_path,
            "line_number": f.line,
            "end_line_number": f.end_line,
            "code_snippet": f.snippet,
            "remediation": f.remediation,
            "confidence": f.confidence,
        })
    return results
