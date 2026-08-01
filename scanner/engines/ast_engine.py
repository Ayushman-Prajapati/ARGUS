"""
ARGUS AST Engine - Orchestrator
==============================
Orchestrates the AST-based static analysis by:
1. Parsing source code into a Python AST
2. Initializing the Rule Registry
3. Loading explicitly registered rules
4. Executing all registered rules
5. Collecting and returning findings in a consistent format

Detection logic is delegated to modular rule implementations.
"""
import ast
import logging
from typing import Any

from scanner.engines.ast.registry import RuleRegistry
from scanner.engines.ast.findings import normalize_findings

logger = logging.getLogger(__name__)


def scan_source(file_path: str, source: str) -> list[dict[str, Any]]:
    """
    Parse `source` and run all registered AST rules against it.

    Returns a list of normalized finding dicts ready to persist as Finding rows.
    Syntax errors are reported as a single low-severity finding so one bad file
    never aborts a whole scan.
    """
    # Parse the source into an AST
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as exc:
        logger.warning("Syntax error parsing %s: %s", file_path, exc.msg)
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

    # Initialize registry (rules are auto-registered from the available
    # rule catalog in scanner/engines/ast/__init__.py)
    registry = RuleRegistry()

    # Execute all rules against the AST
    try:
        raw_findings = registry.execute_all(tree)
    except Exception:
        logger.exception("Unexpected error during rule execution for %s", file_path)
        return []

    # Normalize findings to the standard format
    return normalize_findings(raw_findings, file_path)