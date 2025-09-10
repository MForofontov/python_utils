"""
Schema validation utility using Cerberus for dictionary-based data validation.

This module provides comprehensive schema validation using Cerberus validator
for validating dictionary structures with flexible schema definitions.
"""

from typing import Any

try:
    from cerberus import Validator
    CERBERUS_AVAILABLE = True
except ImportError:
    # Fallback when cerberus is not available
    Validator = None
    CERBERUS_AVAILABLE = False


def validate_cerberus_schema(
    data: dict[str, Any],
    schema: dict[str, Any],
    allow_unknown: bool = False,
    normalize: bool = True,
    param_name: str = "data",
) -> dict[str, Any]:
    r"""
    Validate data against a Cerberus schema definition.

    Uses Cerberus validator to validate dictionary data against flexible
    schema definitions with support for normalization, coercion, and custom rules.

    Parameters
    ----------
    data : dict[str, Any]
        The dictionary data to validate against the schema.
    schema : dict[str, Any]
        Cerberus schema definition dictionary.
    allow_unknown : bool, optional
        Whether to allow fields not defined in schema (by default False).
    normalize : bool, optional
        Whether to normalize data (apply defaults, coercion) (by default True).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "data").

    Returns
    -------
    dict[str, Any]
        Validated and optionally normalized data dictionary.

    Raises
    ------
    ImportError
        If Cerberus is not installed.
    TypeError
        If data or schema are not dictionaries.
    ValueError
        If data fails schema validation.

    Examples
    --------
    >>> schema = {
    ...     'name': {'type': 'string', 'required': True, 'maxlength': 50},
    ...     'age': {'type': 'integer', 'min': 0, 'max': 150},
    ...     'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$'}
    ... }
    >>> data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
    >>> result = validate_cerberus_schema(data, schema)
    >>> result['name']
    'John'

    >>> invalid_data = {'name': 'John', 'age': -5, 'email': 'invalid-email'}
    >>> validate_cerberus_schema(invalid_data, schema)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: data validation failed: age: min value is 0; email: value does not match regex...

    >>> schema_with_defaults = {
    ...     'name': {'type': 'string', 'required': True},
    ...     'active': {'type': 'boolean', 'default': True},
    ...     'tags': {'type': 'list', 'default': []}
    ... }
    >>> minimal_data = {'name': 'Jane'}
    >>> result = validate_cerberus_schema(minimal_data, schema_with_defaults)
    >>> result['active']
    True

    Notes
    -----
    This function provides comprehensive schema validation including:
    - Type validation with coercion support
    - Field requirements and optional fields
    - Value constraints (min, max, length, regex, etc.)
    - Default value application
    - Custom validation rules
    - Nested schema validation
    - List and dictionary validation

    Common Cerberus schema features:
    - 'type': field type ('string', 'integer', 'float', 'boolean', 'dict', 'list')
    - 'required': whether field is mandatory
    - 'default': default value if field is missing
    - 'min'/'max': numeric range constraints
    - 'minlength'/'maxlength': string/list length constraints
    - 'regex': regular expression pattern for strings
    - 'allowed': list of allowed values
    - 'schema': nested schema for dict/list elements

    Requires the 'cerberus' package to be installed.

    Complexity
    ----------
    Time: O(n) where n is the number of fields and nested structures
    Space: O(n) for creating normalized data copy
    """
    # Check if Cerberus is available
    if not CERBERUS_AVAILABLE:
        raise ImportError(
            "Cerberus is required for schema validation. "
            "Install it with: pip install cerberus"
        )

    # Validate input parameters
    if not isinstance(data, dict):
        raise TypeError(f"{param_name} must be a dictionary, got {type(data).__name__}")

    if not isinstance(schema, dict):
        raise TypeError(f"schema must be a dictionary, got {type(schema).__name__}")

    if not isinstance(allow_unknown, bool):
        raise TypeError(f"allow_unknown must be bool, got {type(allow_unknown).__name__}")

    if not isinstance(normalize, bool):
        raise TypeError(f"normalize must be bool, got {type(normalize).__name__}")

    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    # Create validator instance
    validator = Validator(schema, allow_unknown=allow_unknown)

    # Validate the data
    if normalize:
        # Validate and normalize (applies defaults, coercion, etc.)
        normalized_data = validator.normalized(data)
        if normalized_data is None:
            # Validation failed
            error_details = []
            for field, errors in validator.errors.items():
                if isinstance(errors, list):
                    field_errors = "; ".join(str(error) for error in errors)
                else:
                    field_errors = str(errors)
                error_details.append(f"{field}: {field_errors}")

            formatted_errors = "; ".join(error_details)
            raise ValueError(f"{param_name} validation failed: {formatted_errors}")

        return normalized_data
    else:
        # Validate without normalization
        is_valid = validator.validate(data)
        if not is_valid:
            error_details = []
            for field, errors in validator.errors.items():
                if isinstance(errors, list):
                    field_errors = "; ".join(str(error) for error in errors)
                else:
                    field_errors = str(errors)
                error_details.append(f"{field}: {field_errors}")

            formatted_errors = "; ".join(error_details)
            raise ValueError(f"{param_name} validation failed: {formatted_errors}")

        return data.copy()  # Return a copy to avoid modifying original


__all__ = ['validate_cerberus_schema']
