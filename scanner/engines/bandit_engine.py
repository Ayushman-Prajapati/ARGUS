"""Wrapper around the Bandit CLI (JSON output) normalized into ARGUS findings."""
import json
import subprocess

BANDIT_SEVERITY_MAP = {
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
}


def run_bandit(target_path: str, timeout: int = 120) -> tuple[list[dict], str]:
    """Run bandit -r -f json against target_path.

    Returns (findings, error_message). findings is [] and error_message is set
    if bandit is not installed or fails to run; a non-zero bandit exit code is
    normal (it means findings were found) and is not treated as an error.
    """
    try:
        proc = subprocess.run(
            ["bandit", "-r", target_path, "-f", "json", "-q"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return [], ("Bandit is not installed in this environment. "
                     "Install it with `pip install bandit`.")
    except subprocess.TimeoutExpired:
        return [], f"Bandit scan timed out after {timeout}s."

    if not proc.stdout.strip():
        if proc.returncode not in (0, 1):
            return [], f"Bandit exited with code {proc.returncode}: {proc.stderr[:500]}"
        return [], ""

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], "Could not parse Bandit JSON output."

    findings = []
    for item in data.get("results", []):
        severity = BANDIT_SEVERITY_MAP.get(item.get("issue_severity", "MEDIUM"), "medium")
        findings.append({
            "rule_id": item.get("test_id", "BANDIT"),
            "title": item.get("test_name", "Bandit finding"),
            "severity": severity,
            "description": item.get("issue_text", ""),
            "cwe_id": f"CWE-{item['issue_cwe']['id']}" if item.get("issue_cwe") else "",
            "file_path": item.get("filename", ""),
            "line_number": item.get("line_number", 0),
            "end_line_number": item.get("line_range", [None, None])[-1] if item.get("line_range") else None,
            "code_snippet": item.get("code", ""),
            "remediation": item.get("more_info", ""),
            "confidence": item.get("issue_confidence", "").lower(),
        })
    return findings, ""
