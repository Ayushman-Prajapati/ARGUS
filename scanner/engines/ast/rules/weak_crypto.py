"""
Weak Cryptography Detection Rule
=================================
Detects usage of cryptographic primitives and modes that are widely
considered insecure:

Weak hash algorithms
--------------------
- hashlib.md5(), hashlib.sha1()
- hashlib.new("md5"), hashlib.new("sha1")

Weak cipher algorithms
----------------------
- Crypto.Cipher.DES, Crypto.Cipher.ARC4, Crypto.Cipher.Blowfish
- cryptography.hazmat.primitives.ciphers.algorithms.DES,
  cryptography.hazmat.primitives.ciphers.algorithms.ARC4

Insecure cipher modes
---------------------
- ECB mode: AES.MODE_ECB, modes.ECB()

Strong primitives (sha256, sha512, AES-GCM/CBC/CTR, ChaCha20, Fernet, etc.)
are not reported.

Calls and references are resolved to their fully-qualified name using the
same AST-based import analysis as the Command Injection and Unsafe
Deserialization rules, so aliased imports are detected too:

    import hashlib as h
    h.md5(data)                  # resolved to hashlib.md5

    from Crypto.Cipher import DES
    DES.new(key, DES.MODE_ECB)   # resolved to Crypto.Cipher.DES

This sprint detects usage of weak cryptographic primitives only. No misuse
analysis, random-number analysis, key-length validation, or padding checks
are performed.

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

# Weak hash algorithms reported by fully-qualified name.
_WEAK_HASHES = {
    "hashlib.md5": "MD5",
    "hashlib.sha1": "SHA-1",
}

# Weak cipher algorithms reported by fully-qualified name.
_WEAK_CIPHERS = {
    "Crypto.Cipher.DES": "DES",
    "Crypto.Cipher.ARC4": "ARC4",
    "Crypto.Cipher.Blowfish": "Blowfish",
    "cryptography.hazmat.primitives.ciphers.algorithms.DES": "DES",
    "cryptography.hazmat.primitives.ciphers.algorithms.ARC4": "ARC4",
}

# Insecure ECB cipher modes reported by fully-qualified name.
_ECB_MODES = {
    "AES.MODE_ECB": "ECB",
    "cryptography.hazmat.primitives.ciphers.modes.ECB": "ECB",
}

# Attribute names that indicate ECB mode on any cipher class, e.g.
# AES.MODE_ECB, DES.MODE_ECB, or 3DES.MODE_ECB.
_ECB_MODE_ATTRIBUTES = {"MODE_ECB"}

# Weak algorithm names accepted by hashlib.new().
_WEAK_NEW_HASHES = {"md5", "sha1"}

# Per-algorithm severity overrides, keyed by the algorithm display name.
# Defaults: hashes and ECB mode are medium, ciphers are high. SHA-1 is
# broken for collision resistance and is escalated to high; Blowfish is a
# weaker cipher and is downgraded to medium.
_ALGORITHM_SEVERITIES = {
    "SHA-1": "high",
    "SHA1": "high",
    "Blowfish": "medium",
}


def _truncate_snippet(snippet: str) -> str:
    """Trim a single-line snippet to a safe display length."""
    if len(snippet) <= MAX_SNIPPET_LENGTH:
        return snippet
    return snippet[: MAX_SNIPPET_LENGTH - 3] + "..."


class WeakCryptoRule(BaseRule):
    """
    Reports usage of weak hash algorithms, weak cipher algorithms, and ECB
    cipher mode.

    The rule builds a module-wide import map from the AST, then reports any
    call or attribute reference whose fully-qualified name matches a weak
    cryptographic primitive. Import aliases are resolved so ``import hashlib
    as h`` and ``from Crypto.Cipher import DES`` are detected alongside the
    literal dotted forms.
    """

    id = "ARGUS-AST-106"
    name = "Weak Cryptography"
    description = (
        "Detects usage of cryptographically weak or broken primitives: "
        "MD5/SHA-1 hashing, DES/ARC4/Blowfish ciphers, and ECB cipher mode."
    )
    severity = "medium"
    confidence = "medium"
    cwe = "CWE-327"
    owasp = "A02:2021"

    def visit(self, tree: Any) -> list[dict[str, Any]]:
        """
        Analyze the AST tree and return findings for weak cryptography usage.

        Args:
            tree: An ``ast.AST`` tree (typically a parsed Module).

        Returns:
            A list of normalized finding dicts, one per weak primitive.
            Empty list when no weak cryptography is used.
        """
        if not isinstance(tree, ast.AST):
            logger.warning(
                "WeakCryptoRule.visit received non-AST object: %s",
                type(tree).__name__,
            )
            return []

        import_map = _build_import_map(tree)
        parent_map = _build_parent_map(tree)
        findings: list[dict[str, Any]] = []
        # Call nodes already reported, keyed by id() so the same-line dedupe
        # only suppresses each call's own function reference.
        reported_call_ids: set[int] = set()

        # Report bare weak-cipher receivers (DES.new(...)) first so the
        # enclosing call on the same line is not double-reported.
        for node, algorithm in self._weak_cipher_receiver_calls(tree):
            findings.append(self._build_finding(node, "Crypto.Cipher", "Cipher", algorithm))
            reported_call_ids.add(id(node))

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                dotted_name = _resolve_reference_name(node.func, import_map)
                finding = self._classify(dotted_name, node)
                if finding:
                    findings.append(finding)
                    reported_call_ids.add(id(node))
                    continue

                # hashlib.new("md5") style dynamic algorithm selection.
                if dotted_name == "hashlib.new":
                    alg = _hashlib_new_algorithm(node)
                    if alg in _WEAK_NEW_HASHES:
                        findings.append(self._build_finding(
                            node, "hashlib.new", "Hash", alg.upper()
                        ))
                        reported_call_ids.add(id(node))
                    continue

            if isinstance(node, ast.Attribute):
                # Skip an attribute that is the function of a call already
                # reported on this line -- it is the same finding, not a new
                # one. Distinct attributes on the same line (e.g. AES.MODE_ECB
                # inside a DES.new call) are still reported.
                parent = parent_map.get(node)
                if isinstance(parent, ast.Call) and parent.func is node and id(parent) in reported_call_ids:
                    continue

                # Any cipher's MODE_ECB constant, e.g. AES.MODE_ECB or an
                # aliased AES.MODE_ECB, indicates ECB mode.
                if node.attr in _ECB_MODE_ATTRIBUTES:
                    findings.append(self._build_finding(node, "MODE_ECB", "ECB", "ECB"))
                    continue

                dotted_name = _resolve_reference_name(node, import_map)
                finding = self._classify(dotted_name, node)
                if finding:
                    findings.append(finding)

        return findings

    def _weak_cipher_receiver_calls(self, tree: ast.AST) -> list[tuple[ast.Call, str]]:
        """
        Return weak cipher calls where the cipher is a bare receiver of
        ``.new()``/constructor.

        Handles ``DES.new(key)`` and ``Blowfish.new(key)`` where the weak
        cipher is a bare imported name, not an attribute chain.
        """
        import_map = _build_import_map(tree)
        result: list[tuple[ast.Call, str]] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "new":
                continue
            receiver = node.func.value
            if not isinstance(receiver, ast.Name):
                continue
            dotted = import_map.get(receiver.id)
            if dotted in _WEAK_CIPHERS:
                result.append((node, _WEAK_CIPHERS[dotted]))

        return result

    def _classify(self, dotted_name: str, node: ast.AST) -> dict[str, Any] | None:
        """Return a finding dict for a weak primitive, or None if not weak."""
        if dotted_name in _WEAK_HASHES:
            return self._build_finding(node, dotted_name, "Hash", _WEAK_HASHES[dotted_name])
        if dotted_name in _WEAK_CIPHERS:
            return self._build_finding(node, dotted_name, "Cipher", _WEAK_CIPHERS[dotted_name])
        if dotted_name in _ECB_MODES:
            return self._build_finding(node, dotted_name, "ECB", _ECB_MODES[dotted_name])
        return None

    def _build_finding(
        self,
        node: ast.AST,
        dotted_name: str,
        kind: str,
        algorithm: str,
    ) -> dict[str, Any]:
        """Build a normalized finding dict for a weak crypto reference."""
        default_severity = "high" if kind == "Cipher" else "medium"
        severity = _ALGORITHM_SEVERITIES.get(algorithm, default_severity)
        snippet = _truncate_snippet(ast.unparse(node))

        if kind == "Hash":
            title = f"Weak hash algorithm: {algorithm}"
            description = (
                f"{algorithm} is cryptographically broken for collision "
                "resistance and unsuitable for security-sensitive use."
            )
            remediation = (
                "Use hashlib.sha256() or better for security purposes; use a "
                "dedicated password-hashing function (bcrypt/scrypt/argon2) "
                "for credentials."
            )
        elif kind == "Cipher":
            title = f"Weak cipher algorithm: {algorithm}"
            description = (
                f"{algorithm} is a weak or broken cipher that is no longer "
                "considered secure for protecting data."
            )
            remediation = (
                "Use a modern authenticated cipher such as AES-GCM, and "
                "prefer high-level libraries like cryptography or Fernet."
            )
        else:  # ECB
            title = "Insecure cipher mode: ECB"
            description = (
                "ECB mode encrypts each block independently, so identical "
                "plaintext blocks produce identical ciphertext blocks, "
                "leaking data patterns."
            )
            remediation = (
                "Use an authenticated mode such as AES-GCM, or at minimum "
                "CBC/CTR with a unique IV per message. Never use ECB."
            )

        return {
            "rule_id": self.id,
            "title": title,
            "description": description,
            "severity": severity,
            "confidence": self.confidence,
            "cwe_id": self.cwe,
            "owasp_category": self.owasp,
            "line_number": getattr(node, "lineno", 0),
            "end_line_number": getattr(node, "end_lineno", None),
            "code_snippet": snippet,
            "remediation": remediation,
        }


# ---------------------------------------------------------------------------
# Import-aware reference resolution helpers
# ---------------------------------------------------------------------------


def _build_parent_map(tree: ast.AST) -> dict[Any, Any]:
    """Map each node to its parent node in the AST."""
    parent_map: dict[Any, Any] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent_map[child] = node
    return parent_map


def _build_import_map(tree: ast.AST) -> dict[str, str]:
    """
    Map every local name to the fully-qualified name it refers to.

    Handles ``import hashlib``, ``import hashlib as h``, ``from Crypto.Cipher
    import DES``, and nested imports such as ``from cryptography.hazmat.
    primitives.ciphers import algorithms``.
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


def _resolve_reference_name(func: Any, import_map: dict[str, str]) -> str:
    """
    Resolve a name/attribute reference to its fully-qualified dotted name.

    - ``hashlib.md5`` -> ``hashlib.md5``
    - ``h.md5`` (import hashlib as h) -> ``hashlib.md5``
    - ``DES`` (from Crypto.Cipher import DES) -> ``Crypto.Cipher.DES``
    - ``modes.ECB`` -> ``cryptography.hazmat.primitives.ciphers.modes.ECB``
    - Unimported bare names resolve to their bare name (never matched).
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


def _hashlib_new_algorithm(node: ast.Call) -> str:
    """
    Return the algorithm name passed to hashlib.new(), or an empty string.

    The algorithm may be the first positional argument or the ``name``
    keyword argument, supplied as a string literal.
    """
    if node.args:
        arg0 = node.args[0]
        if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
            return arg0.value.lower()
    for kw in node.keywords:
        if kw.arg == "name":
            if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return kw.value.value.lower()
    return ""
