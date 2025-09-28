"""
Schema validation utility using Pydantic for complex data structure validation.

This module provides comprehensive schema validation using Pydantic models
for validating complex nested data structures, API payloads, and configuration
objects. The helper supports both Pydantic v1 and v2 by dynamically
configuring models to respect ``allow_extra`` and ``strict`` options for the
requested runtime.
"""

from dataclasses import dataclass
from typing import Any, TypeVar

try:
    from pydantic import BaseModel, ValidationError
    from pydantic.dataclasses import dataclass as pydantic_dataclass

    PYDANTIC_AVAILABLE = True
except ImportError:
    # Fallback classes when pydantic is not available
    BaseModel = object
    ValidationError = Exception
    pydantic_dataclass = dataclass
    PYDANTIC_AVAILABLE = False

try:
    from pydantic import ConfigDict

    HAS_CONFIG_DICT = True
except ImportError:
    ConfigDict = None  # type: ignore[assignment]
    HAS_CONFIG_DICT = False

T = TypeVar("T")


def validate_pydantic_schema(
    data: dict[str, Any] | Any,
    schema_model: type[T],
    strict: bool = True,
    allow_extra: bool = False,
    param_name: str = "data",
) -> T:
    """
    Validate data against a Pydantic schema model.

    Uses Pydantic models to validate complex data structures with type checking,
    field validation, and nested object validation.

    Parameters
    ----------
    data : dict[str, Any] | Any
        The data to validate against the schema.
    schema_model : Type[T]
        Pydantic model class to validate against.
    strict : bool, optional
        Whether to use strict validation mode (by default True).
    allow_extra : bool, optional
        Whether to allow extra fields not defined in schema (by default False).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "data").

    Returns
    -------
    T
        Validated Pydantic model instance.

    Raises
    ------
    ImportError
        If Pydantic is not installed.
    TypeError
        If schema_model is not a Pydantic model or data has wrong type.
    ValueError
        If data fails schema validation.

    Examples
    --------
    >>> from pydantic import BaseModel
    >>> class UserSchema(BaseModel):
    ...     name: str
    ...     age: int
    ...     email: str
    >>>
    >>> data = {"name": "John", "age": 30, "email": "john@example.com"}
    >>> user = validate_pydantic_schema(data, UserSchema)
    >>> user.name
    'John'

    >>> invalid_data = {"name": "John", "age": "thirty", "email": "john@example.com"}
    >>> validate_pydantic_schema(invalid_data, UserSchema)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: data validation failed: age: Input should be a valid integer...

    >>> class NestedSchema(BaseModel):
    ...     user: UserSchema
    ...     created_at: str
    >>>
    >>> nested_data = {
    ...     "user": {"name": "John", "age": 30, "email": "john@example.com"},
    ...     "created_at": "2023-01-01"
    ... }
    >>> result = validate_pydantic_schema(nested_data, NestedSchema)

    Notes
    -----
    This function provides comprehensive schema validation including:
    - Complex nested object validation
    - Type coercion and validation
    - Field-level validators and constraints
    - Custom validation logic through Pydantic models
    - Detailed error messages with field-specific information
    - Support for optional fields, default values, and aliases

    Requires the 'pydantic' package to be installed. The function will raise
    ImportError if Pydantic is not available.

    Complexity
    ----------
    Time: O(n) where n is the number of fields and nested objects
    Space: O(n) for creating the validated model instance
    """
    # Check if Pydantic is available
    if not PYDANTIC_AVAILABLE:
        raise ImportError(
            "Pydantic is required for schema validation. "
            "Install it with: pip install pydantic"
        )

    # Validate input parameters
    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    if not isinstance(strict, bool):
        raise TypeError(f"strict must be bool, got {type(strict).__name__}")

    if not isinstance(allow_extra, bool):
        raise TypeError(f"allow_extra must be bool, got {type(allow_extra).__name__}")

    # Validate that schema_model is a Pydantic model class
    if not (isinstance(schema_model, type) and issubclass(schema_model, BaseModel)):
        raise TypeError(
            f"schema_model must be a Pydantic BaseModel class, got {type(schema_model).__name__}"
        )

    try:
        configured_model = schema_model

        if PYDANTIC_AVAILABLE:
            if HAS_CONFIG_DICT:
                config_dict: dict[str, Any] = {}
                if allow_extra:
                    config_dict["extra"] = "allow"
                else:
                    config_dict["extra"] = "forbid"
                if strict:
                    config_dict["strict"] = True

                if config_dict:
                    configured_model = type(
                        f"{schema_model.__name__}Configured",
                        (schema_model,),
                        {"model_config": ConfigDict(**config_dict)},
                    )
            else:
                config_attrs: dict[str, Any] = {
                    "extra": "allow" if allow_extra else "forbid",
                    "allow_mutation": not strict,
                }
                base_config = getattr(schema_model, "Config", None)
                config_bases: tuple[type, ...]
                if isinstance(base_config, type):
                    config_bases = (base_config,)
                else:
                    config_bases = (object,)

                Config = type(
                    f"{schema_model.__name__}Config",
                    config_bases,
                    config_attrs,
                )

                configured_model = type(
                    f"{schema_model.__name__}Configured",
                    (schema_model,),
                    {"Config": Config},
                )

        # Validate the data
        if isinstance(data, dict):
            validated_instance = configured_model(**data)
        else:
            validated_instance = configured_model(data)

        return validated_instance

    except ValidationError as e:
        # Format validation errors into a readable message
        error_details = []
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            error_msg = error["msg"]
            error_details.append(f"{field_path}: {error_msg}")

        formatted_errors = "; ".join(error_details)
        raise ValueError(f"{param_name} validation failed: {formatted_errors}") from e

    except Exception as e:
        raise ValueError(
            f"{param_name} validation failed with unexpected error: {str(e)}"
        ) from e


__all__ = ["validate_pydantic_schema"]
