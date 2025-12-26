"""
Schema validation functions module.

This module provides comprehensive schema validation utilities using external libraries
like Pydantic and Cerberus for validating complex data structures against defined schemas.

The module focuses on advanced schema-based validation for APIs, configuration files,
and complex data structures.
"""

from .validate_cerberus_schema import validate_cerberus_schema
from .validate_pydantic_schema import validate_pydantic_schema

__all__ = [
    "validate_pydantic_schema",
    "validate_cerberus_schema",
]

from _version import __version__
