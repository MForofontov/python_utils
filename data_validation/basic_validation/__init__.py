"""
Basic data validation functions module.

This module provides fundamental data validation utilities including type checking,
value range validation, collection validation, string validation, and email validation.

The module focuses on basic data type and value validation without complex schema systems.
"""

from .validate_collection import validate_collection
from .validate_email import validate_email
from .validate_range import validate_range
from .validate_string import validate_string
from .validate_type import validate_type

__all__ = [
    "validate_type",
    "validate_range",
    "validate_collection",
    "validate_string",
    "validate_email",
]

