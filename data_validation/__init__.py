"""
Data validation functions module.

This module provides comprehensive data validation utilities organized into two categories:
1. Basic validation - Type checking, value validation, collection validation, string validation
2. Schema validation - Advanced schema validation using Pydantic and Cerberus

The module serves as a central hub for all data validation needs in the library.
"""

# Import from submodules
from .basic_validation import *
from .schema_validation import *

# Re-export all functions for convenience
from .basic_validation import (
    validate_type,
    validate_range,
    validate_collection,
    validate_string,
    validate_email,
)
from .schema_validation import (
    validate_pydantic_schema,
    validate_cerberus_schema,
)

__all__ = [
    # Basic validation functions
    'validate_type',
    'validate_range',
    'validate_collection',
    'validate_string',
    'validate_email',
    # Schema validation functions
    'validate_pydantic_schema',
    'validate_cerberus_schema',
]

__version__ = '1.0.0'
