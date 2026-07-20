"""Wrapper around the Semgrep CLI (JSON output) normalized into ARGUS findings."""
import json
import subprocess

SEMGREP_SEVERITY_MAP = {
    "ERROR": "high",
    "WARNING": "medium",
    "INFO": "low",
}


def run_semgrep(target_path: str, timeout: int = 120, config: str = "auto") -> tuple[list[dict], str]:
    """Run `semgrep --config <config> --json` against target_path.

    Returns (findings, error_message). Network access is required the first
    time `--config auto` pulls the default ruleset; if unavailable, callers
    should fall back to config='p/security-audit' or a bundled local ruleset.
    """
    try:
        proc = subprocess.run(
            ["semgrep", "--config", config, "--json", "--quiet",
             "--timeout", str(timeout), target_path],
            capture_output=True,
            text=True,
            timeout=timeout + 30,
        )
    except FileNotFoundError:
        return [], ("Semgrep is not installed in this environment. "
                     "Install it with `pip install semgrep`.")
    except subprocess.TimeoutExpired:
        return [], f"Semgrep scan timed out after {timeout}s."

    if not proc.stdout.strip():
        return [], (proc.stderr[:500] if proc.returncode not in (0, 1) else "")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], "Could not parse Semgrep JSON output."

    findings = []
    for item in data.get("results", []):
        extra = item.get("extra", {})
        severity = SEMGREP_SEVERITY_MAP.get(extra.get("severity", "WARNING"), "medium")
        metadata = extra.get("metadata", {})
        cwe = metadata.get("cwe", "")
        if isinstance(cwe, list):
            cwe = ", ".join(cwe)
        owasp = metadata.get("owasp", "")
        if isinstance(owasp, list):
            owasp = ", ".join(owasp)

        findings.append({
            "rule_id": item.get("check_id", "SEMGREP"),
            "title": extra.get("message", "Semgrep finding").split(".")[0][:200],
            "severity": severity,
            "description": extra.get("message", ""),
            "cwe_id": cwe,
            "owasp_category": owasp,
            "file_path": item.get("path", ""),
            "line_number": item.get("start", {}).get("line", 0),
            "end_line_number": item.get("end", {}).get("line", None),
            "code_snippet": extra.get("lines", ""),
            "remediation": metadata.get("references", [""])[0] if metadata.get("references") else "",
            "confidence": metadata.get("confidence", "").lower(),
        })
    return findings, ""
