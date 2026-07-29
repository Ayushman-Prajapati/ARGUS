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

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate subclass metadata on creation."""
        super().__init_subclass__(**kwargs)
        if cls is not BaseRule:
            if not cls.id:
                raise ValueError(f"Rule {cls.__name__} must define an 'id'")
            if not cls.name:
                raise ValueError(f"Rule {cls.__name__} must define a 'name'")

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

    def get_metadata(self) -> dict[str, Any]:
        """
        Return the rule's metadata as a dictionary.

        Returns:
            Dictionary containing rule metadata.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
            "confidence": self.confidence,
            "cwe": self.cwe,
            "owasp": self.owasp,
        }

    def __repr__(self) -> str:
        """Return a string representation of the rule."""
        return f"<{self.__class__.__name__}(id={self.id!r}, name={self.name!r})>"