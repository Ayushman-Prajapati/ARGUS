"""
AST Rules Collection
"""
from scanner.engines.ast.rules.command_injection import CommandInjectionRule
from scanner.engines.ast.rules.dangerous_functions import DangerousFunctionRule
from scanner.engines.ast.rules.deserialization import DeserializationRule
from scanner.engines.ast.rules.secrets import SecretDetectionRule
from scanner.engines.ast.rules.sql_injection import SQLInjectionRule

__all__ = [
    "CommandInjectionRule",
    "DangerousFunctionRule",
    "DeserializationRule",
    "SecretDetectionRule",
    "SQLInjectionRule",
]
