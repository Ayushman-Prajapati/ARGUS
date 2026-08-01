"""
ARGUS AST Engine
"""
from scanner.engines.ast.rules import DangerousFunctionRule

# Catalog of AST rules available to the engine. New rules only need to be
# added here to be registered and executed - the engine, registry, and
# BaseRule interface remain unchanged.
available_rules = [
    DangerousFunctionRule(),
]

__all__ = ["available_rules"]
