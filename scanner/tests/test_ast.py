"""
Comprehensive unit tests for the ARGUS AST Engine.

Each rule is tested for:
- Positive cases (vulnerable code produces findings)
- Negative cases (safe code produces zero findings)
- Edge cases (empty source, syntax errors, nesting, aliases, multiples)

The complete pipeline is also validated end to end:
source -> AST parse -> RuleRegistry -> rule execution -> normalization.
"""
import ast
import unittest

from scanner.engines.ast import available_rules
from scanner.engines.ast.base_rule import BaseRule
from scanner.engines.ast.findings import normalize_findings
from scanner.engines.ast.registry import RuleRegistry
from scanner.engines.ast.rules import (
    CommandInjectionRule,
    DangerousFunctionRule,
    DeserializationRule,
    SecretDetectionRule,
    SQLInjectionRule,
    WeakCryptoRule,
)
from scanner.engines.ast_engine import scan_source

# The normalized finding schema every rule must conform to.
NORMALIZED_KEYS = {
    "rule_id",
    "title",
    "description",
    "severity",
    "confidence",
    "cwe_id",
    "owasp_category",
    "file_path",
    "line_number",
    "end_line_number",
    "code_snippet",
    "remediation",
}


def scan(code: str) -> list[dict]:
    """Run the full engine pipeline on a snippet of source code."""
    return scan_source("test.py", code)


def finding_titles(code: str) -> list[str]:
    """Return the titles of all findings for a snippet."""
    return [f["title"] for f in scan(code)]


class RuleSchemaTest(unittest.TestCase):
    """Every registered rule must expose consistent metadata and findings."""

    def test_all_rules_are_base_rules(self):
        for rule in available_rules:
            self.assertIsInstance(rule, BaseRule)

    def test_rule_metadata_present(self):
        for rule in available_rules:
            self.assertTrue(rule.id)
            self.assertTrue(rule.name)
            self.assertTrue(rule.description)
            self.assertIn(rule.severity, {"critical", "high", "medium", "low", "info"})
            self.assertIn(rule.confidence, {"high", "medium", "low"})
            self.assertTrue(rule.cwe)
            self.assertTrue(rule.owasp)

    def test_rule_ids_are_unique(self):
        ids = [rule.id for rule in available_rules]
        self.assertEqual(len(ids), len(set(ids)))

    def test_registry_auto_registers_all_rules(self):
        registry = RuleRegistry()
        names = {type(rule).__name__ for rule in registry.list_rules()}
        self.assertEqual(names, {
            "DangerousFunctionRule",
            "CommandInjectionRule",
            "SQLInjectionRule",
            "DeserializationRule",
            "SecretDetectionRule",
            "WeakCryptoRule",
        })

    def test_registry_execute_with_no_rules_returns_empty(self):
        registry = RuleRegistry()
        for rule in list(registry.list_rules()):
            registry.unregister(rule)
        self.assertEqual(registry.execute_all(ast.parse("x = 1")), [])


class PipelineTest(unittest.TestCase):
    """Validate the full engine pipeline and normalization."""

    def test_pipeline_returns_normalized_findings(self):
        findings = scan("import os\neval(x)\nos.system(cmd)")
        self.assertTrue(findings)
        for finding in findings:
            self.assertEqual(set(finding.keys()), NORMALIZED_KEYS)

    def test_normalize_findings_consistent_schema(self):
        raw = [{
            "rule_id": "TEST-1",
            "title": "Test",
            "severity": "high",
            "description": "desc",
            "confidence": "medium",
            "cwe_id": "CWE-999",
            "owasp_category": "A03:2021",
            "line_number": 1,
            "end_line_number": 1,
            "code_snippet": "x",
            "remediation": "fix",
        }]
        normalized = normalize_findings(raw, "f.py")
        self.assertEqual(len(normalized), 1)
        self.assertEqual(set(normalized[0].keys()), NORMALIZED_KEYS)
        self.assertEqual(normalized[0]["file_path"], "f.py")

    def test_normalize_filters_non_dict_findings(self):
        self.assertEqual(normalize_findings(["not a dict", 42, None], "f.py"), [])

    def test_normalize_supports_legacy_keys(self):
        raw = [{
            "rule_id": "TEST-1",
            "name": "legacy name",
            "severity": "low",
            "cwe": "CWE-1",
            "owasp": "A01:2021",
            "line": 5,
            "end_line": 6,
            "snippet": "code",
        }]
        normalized = normalize_findings(raw, "f.py")[0]
        self.assertEqual(normalized["title"], "legacy name")
        self.assertEqual(normalized["cwe_id"], "CWE-1")
        self.assertEqual(normalized["owasp_category"], "A01:2021")
        self.assertEqual(normalized["line_number"], 5)
        self.assertEqual(normalized["end_line_number"], 6)
        self.assertEqual(normalized["code_snippet"], "code")

    def test_syntax_error_returns_controlled_finding(self):
        findings = scan("def broken(\n")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "ARGUS-AST-000")
        self.assertEqual(findings[0]["severity"], "info")
        self.assertTrue(findings[0]["description"])

    def test_empty_source_returns_no_findings(self):
        self.assertEqual(scan(""), [])
        self.assertEqual(scan("\n\n\n"), [])

    def test_file_path_propagates(self):
        findings = scan_source("src/foo.py", "eval(x)")
        self.assertTrue(findings)
        for finding in findings:
            self.assertEqual(finding["file_path"], "src/foo.py")


class DangerousFunctionRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-101 (eval/exec/compile)."""

    def setUp(self):
        self.rule = DangerousFunctionRule()

    def test_detects_eval(self):
        self.assertEqual(len(scan("eval(x)")), 1)

    def test_detects_exec(self):
        self.assertEqual(len(scan("exec(code)")), 1)

    def test_detects_compile(self):
        self.assertEqual(len(scan('compile(src, "f", "exec")')), 1)

    def test_multiple_calls_multiple_findings(self):
        self.assertEqual(len(scan("eval(x)\nexec(y)\ncompile(z, 'f', 'exec')")), 3)

    def test_safe_code_no_findings(self):
        self.assertEqual(scan("def f(x):\n    return x + 1"), [])

    def test_string_references_not_detected(self):
        self.assertEqual(scan("s = 'eval(user_input)'"), [])

    def test_attribute_calls_not_detected(self):
        self.assertEqual(scan("obj.eval(x)\nobj.exec(y)\nobj.compile(z)"), [])

    def test_shadowed_name_not_detected(self):
        self.assertEqual(scan("def eval(x):\n    return x\neval(1)"), [])

    def test_nested_function_detection(self):
        code = "def outer():\n    def inner():\n        return eval(x)\n    return inner()"
        self.assertEqual(len(scan(code)), 1)

    def test_class_method_detection(self):
        code = "class C:\n    def m(self):\n        return exec(y)"
        self.assertEqual(len(scan(code)), 1)

    def test_module_scope_shadow_skips_all(self):
        code = "eval = custom\neval(x)\ndef f():\n    eval(y)"
        self.assertEqual(scan(code), [])

    def test_finding_metadata(self):
        finding = scan("eval(x)")[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-101")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["cwe_id"], "CWE-95")
        self.assertEqual(finding["owasp_category"], "A03:2021")
        self.assertEqual(finding["line_number"], 1)
        self.assertEqual(finding["code_snippet"], "eval(x)")


class CommandInjectionRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-102 (os/subprocess command execution)."""

    def setUp(self):
        self.rule = CommandInjectionRule()

    def test_detects_all_apis(self):
        code = (
            "import os, subprocess\n"
            "os.system(cmd)\n"
            "os.popen(cmd)\n"
            "subprocess.run(cmd)\n"
            "subprocess.Popen(cmd)\n"
            "subprocess.call(cmd)\n"
            "subprocess.check_call(cmd)\n"
            "subprocess.check_output(cmd)\n"
        )
        self.assertEqual(len(scan(code)), 7)

    def test_import_alias_resolution(self):
        self.assertEqual(len(scan("import subprocess as sp\nsp.run(cmd)")), 1)
        self.assertEqual(len(scan("import os as o\no.system(cmd)")), 1)

    def test_from_import_resolution(self):
        self.assertEqual(len(scan("from subprocess import run\nrun(cmd)")), 1)
        self.assertEqual(len(scan("from os import system\nsystem(cmd)")), 1)

    def test_unimported_bare_name_not_detected(self):
        self.assertEqual(scan("run(cmd)\nsystem(cmd)"), [])

    def test_safe_code_no_findings(self):
        self.assertEqual(scan("def f():\n    return subprocess.run"), [])
        self.assertEqual(scan("x = 1"), [])

    def test_similar_names_not_detected(self):
        self.assertEqual(scan("os.systemic(cmd)\nsubprocess.runner(cmd)"), [])

    def test_non_module_attribute_not_detected(self):
        self.assertEqual(scan("obj.os.system(cmd)"), [])

    def test_multiple_apis_multiple_findings(self):
        self.assertEqual(len(scan("import os\nos.system(a)\nos.popen(b)")), 2)

    def test_finding_metadata(self):
        finding = scan("import os\nos.system(cmd)")[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-102")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["cwe_id"], "CWE-78")
        self.assertEqual(finding["line_number"], 2)


class SQLInjectionRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-103 (unsafe SQL construction)."""

    def setUp(self):
        self.rule = SQLInjectionRule()

    def test_detects_concat(self):
        self.assertEqual(len(scan('cur.execute("SELECT * FROM u WHERE id = " + uid)')), 1)

    def test_detects_percent_format(self):
        self.assertEqual(len(scan('cur.execute("SELECT * FROM u WHERE id = %s" % uid)')), 1)

    def test_detects_format_method(self):
        self.assertEqual(len(scan('cur.execute("SELECT * FROM u WHERE id = {}".format(uid))')), 1)

    def test_detects_fstring(self):
        self.assertEqual(len(scan('cur.execute(f"SELECT * FROM u WHERE id = {uid}")')), 1)

    def test_detects_executemany(self):
        self.assertEqual(len(scan('cur.executemany("INSERT INTO u VALUES (%s)" % rows)')), 1)

    def test_parameterized_not_reported(self):
        self.assertEqual(scan('cur.execute("SELECT * FROM u WHERE id = %s", (uid,))'), [])
        self.assertEqual(scan('cur.execute("SELECT * FROM u WHERE id = ?", (uid,))'), [])
        self.assertEqual(scan('cur.execute("SELECT * FROM u WHERE id = %s", {"id": uid})'), [])

    def test_parameterized_kwarg_not_reported(self):
        self.assertEqual(scan('cur.execute("SELECT * FROM u WHERE id = %s", params=(uid,))'), [])

    def test_literal_sql_not_reported(self):
        self.assertEqual(scan('cur.execute("SELECT 1")'), [])

    def test_receiver_variants_detected(self):
        code = (
            'cursor.execute("SELECT * FROM u WHERE id = " + uid)\n'
            'connection.execute("SELECT * FROM u WHERE id = " + uid)\n'
            'session.execute("SELECT * FROM u WHERE id = " + uid)\n'
            'db.get_cursor().execute("SELECT * FROM u WHERE id = " + uid)\n'
        )
        self.assertEqual(len(scan(code)), 4)

    def test_bare_execute_not_reported(self):
        self.assertEqual(scan('execute("SELECT " + x)'), [])

    def test_plain_format_not_sql(self):
        self.assertEqual(scan('x = "SELECT {}".format(y)'), [])

    def test_safe_code_no_findings(self):
        self.assertEqual(scan("def f(x):\n    return x + 1"), [])

    def test_finding_metadata(self):
        finding = scan('cur.execute("SELECT * FROM u WHERE id = " + uid)')[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-103")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["cwe_id"], "CWE-89")
        self.assertEqual(finding["owasp_category"], "A03:2021")


class DeserializationRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-104 (unsafe deserialization APIs)."""

    def setUp(self):
        self.rule = DeserializationRule()

    def test_detects_all_apis(self):
        code = (
            "import pickle, cPickle, dill, marshal, shelve, yaml\n"
            "pickle.load(f)\npickle.loads(d)\n"
            "cPickle.load(f)\ncPickle.loads(d)\n"
            "dill.load(f)\ndill.loads(d)\n"
            "marshal.load(f)\nmarshal.loads(d)\n"
            "shelve.open('db')\nyaml.load(s)\n"
        )
        self.assertEqual(len(scan(code)), 10)

    def test_yaml_safe_load_not_reported(self):
        self.assertEqual(scan("import yaml\nyaml.safe_load(s)"), [])

    def test_yaml_load_safe_loader_not_reported(self):
        self.assertEqual(scan("import yaml\nyaml.load(s, Loader=yaml.SafeLoader)"), [])
        self.assertEqual(scan("import yaml\nyaml.load(s, Loader=yaml.CSafeLoader)"), [])

    def test_yaml_load_unsafe_loader_reported(self):
        self.assertEqual(len(scan("import yaml\nyaml.load(s, Loader=yaml.UnsafeLoader)")), 1)
        self.assertEqual(len(scan("import yaml\nyaml.load(s)")), 1)

    def test_import_alias_resolution(self):
        self.assertEqual(len(scan("import pickle as p\np.loads(d)")), 1)
        self.assertEqual(len(scan("from yaml import load\nload(s)")), 1)
        self.assertEqual(len(scan("from pickle import loads as pl\npl(d)")), 1)

    def test_unimported_bare_name_not_detected(self):
        self.assertEqual(scan("loads(d)\nload(s)"), [])

    def test_similar_names_not_detected(self):
        self.assertEqual(scan("import pickle\npickle.loader(f)\nyaml.safe_loads(s)"), [])

    def test_severity_levels(self):
        pickle_finding = scan("import pickle\npickle.loads(d)")[0]
        self.assertEqual(pickle_finding["severity"], "critical")
        yaml_finding = scan("import yaml\nyaml.load(s)")[0]
        self.assertEqual(yaml_finding["severity"], "high")

    def test_finding_metadata(self):
        finding = scan("import pickle\npickle.loads(d)")[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-104")
        self.assertEqual(finding["cwe_id"], "CWE-502")
        self.assertEqual(finding["owasp_category"], "A03:2021")


class SecretDetectionRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-105 (hardcoded secrets)."""

    def setUp(self):
        self.rule = SecretDetectionRule()

    def test_detects_various_secrets(self):
        code = (
            'password = "admin123"\n'
            'SECRET_KEY = "django-secret"\n'
            'API_KEY = "abcd1234"\n'
            'TOKEN = "eyJhbGciOiJIUzI1NiIs..."\n'
        )
        self.assertEqual(len(scan(code)), 4)

    def test_database_url_not_reported(self):
        # database_url is a generic configuration variable, not a credential,
        # and was deliberately removed from the secret hints.
        self.assertEqual(scan('database_url = "postgres://user:pass@host/db"'), [])

    def test_detects_short_secret(self):
        self.assertEqual(len(scan('PASSWORD = "x"')), 1)

    def test_empty_secret_not_reported(self):
        self.assertEqual(scan('PASSWORD = ""'), [])
        self.assertEqual(scan('PASSWORD = " "'), [])

    def test_runtime_sources_not_reported(self):
        self.assertEqual(scan('password = os.getenv("PASSWORD")'), [])
        self.assertEqual(scan('SECRET_KEY = environ["SECRET_KEY"]'), [])
        self.assertEqual(scan("API_KEY = settings.API_KEY"), [])
        self.assertEqual(scan('DATABASE_URL = config["database_url"]'), [])
        self.assertEqual(scan("token = get_token()"), [])

    def test_imported_constant_not_reported(self):
        self.assertEqual(scan("from config import API_KEY\nAPI_KEY"), [])

    def test_non_string_value_not_reported(self):
        self.assertEqual(scan("password = 12345"), [])
        self.assertEqual(scan("password = True"), [])

    def test_benign_lookalikes_not_reported(self):
        self.assertEqual(scan('password_reset = "https://x"'), [])
        self.assertEqual(scan("tokenize = 1"), [])

    def test_prefixed_names_detected(self):
        self.assertEqual(len(scan('my_password = "s3cret"')), 1)
        self.assertEqual(len(scan('_SECRET_KEY = "abc123"')), 1)

    def test_unpacking_not_reported(self):
        self.assertEqual(scan('a, b = password, "x"'), [])

    def test_multiple_secrets_multiple_findings(self):
        self.assertEqual(len(scan('password = "x123"\nAPI_KEY = "y123"\nTOKEN = "z123"')), 3)

    def test_finding_metadata(self):
        finding = scan('password = "admin123"')[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-105")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["cwe_id"], "CWE-798")
        self.assertEqual(finding["owasp_category"], "A03:2021")


class WeakCryptoRuleTest(unittest.TestCase):
    """Tests for ARGUS-AST-106 (weak cryptography)."""

    def setUp(self):
        self.rule = WeakCryptoRule()

    def test_detects_weak_hashes(self):
        self.assertEqual(len(scan("import hashlib\nhashlib.md5(d)")), 1)
        self.assertEqual(len(scan("import hashlib\nhashlib.sha1(d)")), 1)

    def test_detects_hashlib_new(self):
        self.assertEqual(len(scan('import hashlib\nhashlib.new("md5")')), 1)
        self.assertEqual(len(scan('import hashlib\nhashlib.new(name="sha1")')), 1)

    def test_strong_hashes_not_reported(self):
        self.assertEqual(scan("import hashlib\nhashlib.sha256(d)"), [])
        self.assertEqual(scan("import hashlib\nhashlib.sha512(d)"), [])
        self.assertEqual(scan("import hashlib\nhashlib.blake2b(d)"), [])

    def test_detects_weak_ciphers(self):
        self.assertEqual(len(scan("from Crypto.Cipher import DES\nDES.new(k)")), 1)
        self.assertEqual(len(scan("from Crypto.Cipher import ARC4\nARC4.new(k)")), 1)
        self.assertEqual(len(scan("from Crypto.Cipher import Blowfish\nBlowfish.new(k)")), 1)

    def test_detects_cryptography_algorithms(self):
        imp = "from cryptography.hazmat.primitives.ciphers import algorithms"
        self.assertEqual(len(scan(imp + "\nalgorithms.DES(k)")), 1)
        self.assertEqual(len(scan(imp + "\nalgorithms.ARC4(k)")), 1)

    def test_detects_ecb_modes(self):
        self.assertEqual(len(scan("from Crypto.Cipher import AES\nAES.MODE_ECB")), 1)
        imp = "from cryptography.hazmat.primitives.ciphers import modes"
        self.assertEqual(len(scan(imp + "\nmodes.ECB()")), 1)

    def test_safe_modes_not_reported(self):
        self.assertEqual(scan("from Crypto.Cipher import AES\nAES.new(k, AES.MODE_GCM)"), [])
        self.assertEqual(scan("from Crypto.Cipher import AES\nAES.new(k, AES.MODE_CBC)"), [])
        imp = "from cryptography.hazmat.primitives.ciphers import modes"
        self.assertEqual(scan(imp + "\nmodes.GCM(iv)"), [])

    def test_aliases_resolved(self):
        self.assertEqual(len(scan("import hashlib as h\nh.md5(d)")), 1)
        self.assertEqual(len(scan("from Crypto.Cipher import DES as D\nD.new(k)")), 1)

    def test_no_double_report(self):
        self.assertEqual(len(scan("import hashlib\nhashlib.md5(d)")), 1)
        self.assertEqual(len(scan("from Crypto.Cipher import DES, AES\nDES.new(k, AES.MODE_ECB)")), 2)

    def test_severity_levels(self):
        md5 = scan("import hashlib\nhashlib.md5(d)")[0]
        sha1 = scan("import hashlib\nhashlib.sha1(d)")[0]
        blowfish = scan("from Crypto.Cipher import Blowfish\nBlowfish.new(k)")[0]
        des = scan("from Crypto.Cipher import DES\nDES.new(k)")[0]
        self.assertEqual(md5["severity"], "medium")
        self.assertEqual(sha1["severity"], "high")
        self.assertEqual(blowfish["severity"], "medium")
        self.assertEqual(des["severity"], "high")

    def test_finding_metadata(self):
        finding = scan("import hashlib\nhashlib.md5(d)")[0]
        self.assertEqual(finding["rule_id"], "ARGUS-AST-106")
        self.assertEqual(finding["cwe_id"], "CWE-327")
        self.assertEqual(finding["owasp_category"], "A02:2021")


if __name__ == "__main__":
    unittest.main()
