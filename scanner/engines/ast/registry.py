"""
AST Rule Registry
"""

from collections.abc import Iterable
from typing import Any


class RuleRegistry:
    """
    Central registry for managing AST analysis rules.

    The registry maintains a collection of rule instances and provides
    methods to register, unregister, list, and execute rules against
    an AST tree. It is designed to be generic and reusable across
    different scanning contexts.
    """

    def __init__(self) -> None:
        """Initialize an empty rule registry."""
        self._rules: list[Any] = []

    def register(self, rule: Any) -> None:
        """
        Register a rule instance.

        Args:
            rule: A rule instance that implements a check method
                  accepting an AST tree and returning findings.
        """
        if rule not in self._rules:
            self._rules.append(rule)

    def unregister(self, rule: Any) -> None:
        """
        Unregister a rule instance.

        Args:
            rule: The rule instance to remove from the registry.
        """
        if rule in self._rules:
            self._rules.remove(rule)

    def list_rules(self) -> list[Any]:
        """
        List all registered rule instances.

        Returns:
            A list of registered rule instances.
        """
        return list(self._rules)

    def execute_all(self, tree: Any) -> list[Any]:
        """
        Execute all registered rules against the given AST tree.

        Args:
            tree: The AST tree to analyze.

        Returns:
            A combined list of findings from all registered rules.
            Returns an empty list if no rules are registered.
        """
        findings: list[Any] = []
        for rule in self._rules:
            if hasattr(rule, "check") and callable(rule.check):
                try:
                    rule_findings = rule.check(tree)
                    if rule_findings:
                        if isinstance(rule_findings, Iterable):
                            findings.extend(rule_findings)
                        else:
                            findings.append(rule_findings)
                except Exception:
                    # Rules should handle their own errors; continue with other rules
                    continue
        return findings