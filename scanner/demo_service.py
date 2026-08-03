"""
ARGUS read-only homepage demo scan — static demo data provider.

Everything the homepage demo needs lives here as static constants. The demo
experience is fully client-side: the view simply injects this data as JSON and
the browser renders + animates it. No database records are ever created and no
part of the real scanning pipeline is touched.
"""
# Source code shown in the demo code viewer (the "vulnerable" file).
DEMO_CODE = [
    "import sqlite3",
    "import subprocess",
    "import pickle",
    "",
    "def login(username, password):",
    "    query = f\"SELECT * FROM users WHERE username='{username}'\"",
    "    cursor.execute(query)",
    "",
    "def run(command):",
    "    subprocess.run(command, shell=True)",
    "",
    'secret_key = "sk_live_demo_secret"',
    "",
    'password = "admin123"',
    "",
    "data = pickle.loads(user_input)",
]

# ``line`` is 1-based, matching DEMO_CODE. Detected by the given engine with a
# severity; these use the platform severity colors (Critical/High/Medium/Low).
DEMO_VULNERABILITIES = [
    {
        "line": 10,
        "engine": "Bandit",
        "severity": "high",
        "message": "Bandit detected insecure subprocess usage.",
        "label": "subprocess.run(command, shell=True)",
    },
    {
        "line": 7,
        "engine": "Semgrep",
        "severity": "critical",
        "message": "Semgrep detected SQL Injection.",
        "label": "cursor.execute(query)",
    },
    {
        "line": 12,
        "engine": "ARGUS AST",
        "severity": "critical",
        "message": "ARGUS AST detected Hardcoded Secret.",
        "label": 'secret_key = "sk_live_demo_secret"',
    },
    {
        "line": 16,
        "engine": "ARGUS AST",
        "severity": "high",
        "message": "ARGUS AST detected Unsafe Deserialization.",
        "label": "pickle.loads(user_input)",
    },
]

# Terminal feed: (timestamp, text). Progress is paced 1s per line in JS.
DEMO_TERMINAL = [
    "[00:01] Loading project...",
    "[00:02] Parsing AST...",
    "[00:03] Bandit detected insecure subprocess usage.",
    "[00:04] Semgrep detected SQL Injection.",
    "[00:05] ARGUS AST detected Hardcoded Secret.",
    "[00:06] ARGUS AST detected Unsafe Deserialization.",
    "[00:07] Aggregating findings...",
    "[00:08] Demo Complete",
]

# Temporary demo statistics. Values are client-side only and reset on refresh.
DEMO_STATS = {
    "scans": 1,
    "findings": 4,
    "critical": 2,
    "engines": 3,
}

# Index (into DEMO_TERMINAL / detection order) at which the demo is "complete".
DEMO_STAGES = [
    {"key": "init", "label": "Initializing"},
    {"key": "parsing", "label": "Parsing AST"},
    {"key": "bandit", "label": "Bandit"},
    {"key": "semgrep", "label": "Semgrep"},
    {"key": "ast1", "label": "ARGUS AST"},
    {"key": "ast2", "label": "ARGUS AST"},
    {"key": "aggregate", "label": "Aggregating findings"},
    {"key": "done", "label": "Complete"},
]


def demo_data():
    """Return the full static demo dataset as a JSON-serializable dict."""
    return {
        "code": list(DEMO_CODE),
        "vulnerabilities": [dict(v) for v in DEMO_VULNERABILITIES],
        "terminal": list(DEMO_TERMINAL),
        "stats": dict(DEMO_STATS),
    }