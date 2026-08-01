"""
AST Finding Normalization
"""
import logging
from typing import Any

logger = logging.getLogger(__name__)


def normalize_findings(findings: list[Any], file_path: str) -> list[dict[str, Any]]:
    """
    Normalize findings from various rule implementations into a consistent dict format.

    Args:
        findings: Raw findings from rule executions.
        file_path: The file path being scanned.

    Returns:
        List of normalized finding dictionaries.
    """
    normalized: list[dict[str, Any]] = []

    for finding in findings:
        if not isinstance(finding, dict):
            continue

        normalized.append({
            "rule_id": finding.get("rule_id", ""),
            "title": finding.get("title", finding.get("name", "")),
            "severity": finding.get("severity", "medium"),
            "description": finding.get("description", ""),
            "cwe_id": finding.get("cwe_id", finding.get("cwe", "")),
            "owasp_category": finding.get("owasp_category", finding.get("owasp", "")),
            "file_path": file_path,
            "line_number": finding.get("line_number", finding.get("line", 0)),
            "end_line_number": finding.get("end_line_number", finding.get("end_line", finding.get("line", 0))),
            "code_snippet": finding.get("code_snippet", finding.get("snippet", "")),
            "remediation": finding.get("remediation", ""),
            "confidence": finding.get("confidence", "medium"),
        })

    return normalized