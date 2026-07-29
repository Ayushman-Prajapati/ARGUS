"""
AST Base Rule
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseRule(ABC):
    """
    Abstract base class for all AST analysis rules.

    Every detection rule in the ARGUS AST Engine must inherit from this class.
    It defines the standard interface and metadata contract for rule implementations.

    Subclasses must implement the `visit` method to provide detection logic.
    """

    # Rule metadata - subclasses should override these
    id: str = ""
    name: str = ""
    description: str = ""
    severity: str = "medium"  # critical, high, medium, low, info
    confidence: str = "medium"  # high, medium, low
    cwe: str = ""
    owasp: str = ""

    @abstractmethod
    def visit(self, tree: Any) -> list[Any]:
        """
        Analyze the AST tree and return findings.

        This method must be implemented by subclasses to provide
        vulnerability detection logic.

        Args:
            tree: The AST tree to analyze.

        Returns:
            A list of finding objects (structure defined by subclasses).
        """
        ...

    def __repr__(self) -> str:
        """Return a string representation of the rule."""
        return f"<{self.__class__.__name__}(id={self.id!r}, name={self.name!r})>"