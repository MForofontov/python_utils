"""
String validation utility with pattern matching and content validation.

This module provides comprehensive string validation including length checks,
pattern matching with regex, content validation, and common string formats.
"""

import re
from re import Pattern


def validate_string(
    value: str,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | Pattern[str] | None = None,
    allow_empty: bool = True,
    strip_whitespace: bool = False,
    case_sensitive: bool = True,
    allowed_chars: str | None = None,
    forbidden_chars: str | None = None,
    param_name: str = "value",
) -> None:
    """
    Validate string content, length, and patterns.

    Provides comprehensive string validation including length bounds, regex patterns,
    character restrictions, and whitespace handling.

    Parameters
    ----------
    value : str
        The string value to validate.
    min_length : int | None, optional
        Minimum allowed string length (by default None for no minimum).
    max_length : int | None, optional
        Maximum allowed string length (by default None for no maximum).
    pattern : str | Pattern[str] | None, optional
        Regex pattern that the string must match (by default None).
    allow_empty : bool, optional
        Whether to allow empty strings (by default True).
    strip_whitespace : bool, optional
        Whether to strip whitespace before validation (by default False).
    case_sensitive : bool, optional
        Whether pattern matching is case sensitive (by default True).
    allowed_chars : str | None, optional
        String of allowed characters (by default None for no restriction).
    forbidden_chars : str | None, optional
        String of forbidden characters (by default None for no restriction).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "value").

    Returns
    -------
    None
        This function returns None if validation passes.

    Raises
    ------
    TypeError
        If value is not a string or parameters have wrong types.
    ValueError
        If string fails validation checks.

    Examples
    --------
    >>> validate_string("hello")  # Passes
    >>> validate_string("hello", min_length=3, max_length=10)  # Passes
    >>> validate_string("", allow_empty=False)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: value cannot be empty

    >>> validate_string("hello123", pattern=r"^[a-z]+$")  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: value does not match required pattern: ^[a-z]+$

    >>> validate_string("hello", allowed_chars="helo")  # Passes
    >>> validate_string("hello!", forbidden_chars="!")  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: value contains forbidden character: !

    >>> validate_string("  hello  ", strip_whitespace=True, min_length=5, max_length=5)  # Passes

    Notes
    -----
    This function provides comprehensive string validation including:
    - Type checking for string input
    - Length bounds validation
    - Regex pattern matching with case sensitivity options
    - Character allowlist and blocklist validation
    - Whitespace stripping option
    - Empty string handling
    - Detailed error messages

    When strip_whitespace is True, the string is stripped before all validations
    except the initial type check. The original string is not modified.

    Pattern matching uses re.fullmatch() to ensure the entire string matches
    the pattern, not just a substring.

    Complexity
    ----------
    Time: O(n) where n is string length for character validation, O(n) for regex
    Space: O(1) for most operations, O(n) for regex compilation
    """
    # Validate input parameters
    if not isinstance(value, str):
        raise TypeError(f"{param_name} must be str, got {type(value).__name__}")

    if min_length is not None:
        if not isinstance(min_length, int):
            raise TypeError(
                f"min_length must be int or None, got {type(min_length).__name__}"
            )
        if min_length < 0:
            raise ValueError(f"min_length must be non-negative, got {min_length}")

    if max_length is not None:
        if not isinstance(max_length, int):
            raise TypeError(
                f"max_length must be int or None, got {type(max_length).__name__}"
            )
        if max_length < 0:
            raise ValueError(f"max_length must be non-negative, got {max_length}")

    if min_length is not None and max_length is not None and min_length > max_length:
        raise ValueError(
            f"min_length ({min_length}) cannot be greater than max_length ({max_length})"
        )

    if not isinstance(allow_empty, bool):
        raise TypeError(f"allow_empty must be bool, got {type(allow_empty).__name__}")

    if not isinstance(strip_whitespace, bool):
        raise TypeError(
            f"strip_whitespace must be bool, got {type(strip_whitespace).__name__}"
        )

    if not isinstance(case_sensitive, bool):
        raise TypeError(
            f"case_sensitive must be bool, got {type(case_sensitive).__name__}"
        )

    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    if allowed_chars is not None and not isinstance(allowed_chars, str):
        raise TypeError(
            f"allowed_chars must be str or None, got {type(allowed_chars).__name__}"
        )

    if forbidden_chars is not None and not isinstance(forbidden_chars, str):
        raise TypeError(
            f"forbidden_chars must be str or None, got {type(forbidden_chars).__name__}"
        )

    # Strip whitespace if requested
    validated_value = value.strip() if strip_whitespace else value

    # Validate emptiness
    if not allow_empty and len(validated_value) == 0:
        raise ValueError(f"{param_name} cannot be empty")

    # Validate length bounds
    length = len(validated_value)

    if min_length is not None and length < min_length:
        raise ValueError(
            f"{param_name} length ({length}) is below minimum allowed length ({min_length})"
        )

    if max_length is not None and length > max_length:
        raise ValueError(
            f"{param_name} length ({length}) exceeds maximum allowed length ({max_length})"
        )

    # Validate pattern if provided
    if pattern is not None:
        # Handle both string patterns and compiled Pattern objects
        if isinstance(pattern, str):
            flags = 0 if case_sensitive else re.IGNORECASE
            compiled_pattern = re.compile(pattern, flags)
        elif isinstance(pattern, Pattern):
            compiled_pattern = pattern
        else:
            raise TypeError(
                f"pattern must be str or Pattern, got {type(pattern).__name__}"
            )

        if not compiled_pattern.fullmatch(validated_value):
            pattern_str = pattern if isinstance(pattern, str) else pattern.pattern
            raise ValueError(
                f"{param_name} does not match required pattern: {pattern_str}"
            )

    # Validate allowed characters
    if allowed_chars is not None:
        allowed_set = set(allowed_chars)
        for char in validated_value:
            if char not in allowed_set:
                raise ValueError(f"{param_name} contains disallowed character: {char}")

    # Validate forbidden characters
    if forbidden_chars is not None:
        forbidden_set = set(forbidden_chars)
        for char in validated_value:
            if char in forbidden_set:
                raise ValueError(f"{param_name} contains forbidden character: {char}")


__all__ = ["validate_string"]
