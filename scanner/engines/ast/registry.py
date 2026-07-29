"""
AST Rule Registry
"""

import logging
from typing import Any

from scanner.engines.ast.base_rule import BaseRule

logger = logging.getLogger(__name__)


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
        self._rules: list[BaseRule] = []

    def register(self, rule: BaseRule) -> None:
        """
        Register a rule instance.

        Args:
            rule: A rule instance implementing the BaseRule interface.

        Raises:
            TypeError: If rule is not a BaseRule instance.
            ValueError: If rule metadata is invalid or missing.
        """
        if not isinstance(rule, BaseRule):
            raise TypeError(f"Expected BaseRule instance, got {type(rule).__name__}")

        # Validate required metadata
        if not rule.id:
            raise ValueError(f"Rule {rule.__class__.__name__} must define an 'id'")
        if not rule.name:
            raise ValueError(f"Rule {rule.__class__.__name__} must define a 'name'")

        if rule not in self._rules:
            self._rules.append(rule)

    def unregister(self, rule: BaseRule) -> None:
        """
        Unregister a rule instance.

        Args:
            rule: The rule instance to remove from the registry.
        """
        if rule in self._rules:
            self._rules.remove(rule)

    def list_rules(self) -> list[BaseRule]:
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
            try:
                findings.extend(rule.visit(tree))
            except Exception:
                logger.exception("Rule %s failed during execution", rule.id)
                continue
        return findings