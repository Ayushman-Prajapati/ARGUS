"""
AST Rules Collection
"""
from scanner.engines.ast.rules.command_injection import CommandInjectionRule
from scanner.engines.ast.rules.dangerous_functions import DangerousFunctionRule

__all__ = ["CommandInjectionRule", "DangerousFunctionRule"]
