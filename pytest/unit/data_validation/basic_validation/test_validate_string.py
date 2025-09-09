"""
Unit tests for validate_string function.

This module contains comprehensive tests for the validate_string function,
including length validation, pattern matching, character restrictions, and edge cases.
"""

import pytest
import re
from data_validation import validate_string


def test_validate_string_basic_validation() -> None:
    """
    Test case 1: Basic string validation without constraints.
    """
    # Test simple strings
    validate_string("hello")
    validate_string("Hello World!")
    validate_string("123")
    validate_string("")  # Empty string allowed by default
    
    # Test strings with special characters
    validate_string("user@example.com")
    validate_string("file_name.txt")
    validate_string("path/to/file")


def test_validate_string_length_validation() -> None:
    """
    Test case 2: String length validation with min/max bounds.
    """
    # Test minimum length
    validate_string("hello", min_length=3)
    validate_string("hi", min_length=2)
    
    # Test maximum length
    validate_string("hello", max_length=10)
    validate_string("hello", max_length=5)
    
    # Test both min and max length
    validate_string("hello", min_length=3, max_length=10)
    validate_string("test", min_length=4, max_length=4)  # Exact length


def test_validate_string_empty_string_handling() -> None:
    """
    Test case 3: Empty string handling with allow_empty parameter.
    """
    # Test allow_empty=True (default)
    validate_string("", allow_empty=True)
    validate_string("", min_length=0, max_length=5, allow_empty=True)
    
    # Test non-empty strings with allow_empty=False
    validate_string("hello", allow_empty=False)
    validate_string("a", allow_empty=False)


def test_validate_string_whitespace_stripping() -> None:
    """
    Test case 4: Whitespace stripping functionality.
    """
    # Test with strip_whitespace=True
    validate_string("  hello  ", strip_whitespace=True)
    validate_string("\t\nhello\t\n", strip_whitespace=True)
    
    # Test length validation after stripping
    validate_string("  hello  ", min_length=5, max_length=5, strip_whitespace=True)
    validate_string("   abc   ", min_length=3, max_length=3, strip_whitespace=True)


def test_validate_string_pattern_matching() -> None:
    """
    Test case 5: Regular expression pattern matching.
    """
    # Test simple patterns
    validate_string("abc123", pattern=r"^[a-z]+\d+$")
    validate_string("hello", pattern=r"^[a-z]+$")
    validate_string("123", pattern=r"^\d+$")
    
    # Test email pattern
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    validate_string("user@example.com", pattern=email_pattern)
    
    # Test phone pattern
    phone_pattern = r"^\+?1?-?\(?[0-9]{3}\)?-?[0-9]{3}-?[0-9]{4}$"
    validate_string("123-456-7890", pattern=phone_pattern)


def test_validate_string_case_sensitivity() -> None:
    """
    Test case 6: Case sensitivity in pattern matching.
    """
    # Test case sensitive (default)
    validate_string("hello", pattern=r"^[a-z]+$", case_sensitive=True)
    
    # Test case insensitive
    validate_string("Hello", pattern=r"^[a-z]+$", case_sensitive=False)
    validate_string("HELLO", pattern=r"^[a-z]+$", case_sensitive=False)
    validate_string("HeLLo", pattern=r"^[a-z]+$", case_sensitive=False)


def test_validate_string_character_restrictions() -> None:
    """
    Test case 7: Character allowlist and blocklist validation.
    """
    # Test allowed characters
    validate_string("abc123", allowed_chars="abc123")
    validate_string("hello", allowed_chars="abcdefghijklmnopqrstuvwxyz")
    validate_string("123", allowed_chars="0123456789")
    
    # Test forbidden characters
    validate_string("hello", forbidden_chars="!@#$%^&*()")
    validate_string("abc123", forbidden_chars="xyz")
    validate_string("test", forbidden_chars="!@#")


def test_validate_string_combined_validations() -> None:
    """
    Test case 8: Complex combinations of validation parameters.
    """
    # Test all parameters together
    validate_string(
        "  hello123  ",
        min_length=8,
        max_length=8,
        pattern=r"^[a-z]+\d+$",
        allow_empty=False,
        strip_whitespace=True,
        case_sensitive=True,
        allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789",
        forbidden_chars="!@#$%"
    )
    
    # Test username validation
    validate_string(
        "user_123",
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",
        forbidden_chars=" !@#$%^&*()",
        allow_empty=False
    )


def test_validate_string_type_error_invalid_input() -> None:
    """
    Test case 9: TypeError for non-string input.
    """
    with pytest.raises(TypeError, match="value must be str, got int"):
        validate_string(123)
    
    with pytest.raises(TypeError, match="value must be str, got list"):
        validate_string([1, 2, 3])
    
    with pytest.raises(TypeError, match="value must be str, got NoneType"):
        validate_string(None)
    
    # Test with custom param name
    with pytest.raises(TypeError, match="username must be str, got int"):
        validate_string(123, param_name="username")


def test_validate_string_type_error_invalid_parameters() -> None:
    """
    Test case 10: TypeError for invalid parameter types.
    """
    # Test invalid min_length
    with pytest.raises(TypeError, match="min_length must be int or None, got str"):
        validate_string("hello", min_length="5")
    
    # Test invalid max_length
    with pytest.raises(TypeError, match="max_length must be int or None, got float"):
        validate_string("hello", max_length=5.5)
    
    # Test invalid boolean parameters
    with pytest.raises(TypeError, match="allow_empty must be bool, got str"):
        validate_string("hello", allow_empty="true")
    
    with pytest.raises(TypeError, match="strip_whitespace must be bool, got int"):
        validate_string("hello", strip_whitespace=1)
    
    with pytest.raises(TypeError, match="case_sensitive must be bool, got str"):
        validate_string("hello", case_sensitive="yes")
    
    # Test invalid character restriction parameters
    with pytest.raises(TypeError, match="allowed_chars must be str or None, got list"):
        validate_string("hello", allowed_chars=["a", "b", "c"])
    
    with pytest.raises(TypeError, match="forbidden_chars must be str or None, got int"):
        validate_string("hello", forbidden_chars=123)


def test_validate_string_value_error_empty_not_allowed() -> None:
    """
    Test case 11: ValueError when empty strings are not allowed.
    """
    with pytest.raises(ValueError, match="value cannot be empty"):
        validate_string("", allow_empty=False)
    
    # Test with whitespace stripping
    with pytest.raises(ValueError, match="value cannot be empty"):
        validate_string("   ", allow_empty=False, strip_whitespace=True)
    
    # Test with custom param name
    with pytest.raises(ValueError, match="username cannot be empty"):
        validate_string("", allow_empty=False, param_name="username")


def test_validate_string_value_error_length_violations() -> None:
    """
    Test case 12: ValueError for length constraint violations.
    """
    # Test below minimum length
    with pytest.raises(ValueError, match="value length \\(2\\) is below minimum allowed length \\(5\\)"):
        validate_string("hi", min_length=5)
    
    # Test above maximum length
    with pytest.raises(ValueError, match="value length \\(10\\) exceeds maximum allowed length \\(5\\)"):
        validate_string("hello world", max_length=5)
    
    # Test with custom param name
    with pytest.raises(ValueError, match="password length \\(3\\) is below minimum allowed length \\(8\\)"):
        validate_string("abc", min_length=8, param_name="password")


def test_validate_string_value_error_pattern_mismatch() -> None:
    """
    Test case 13: ValueError for pattern matching failures.
    """
    # Test pattern mismatch
    with pytest.raises(ValueError, match="value does not match required pattern: \\^\\[a-z\\]\\+\\$"):
        validate_string("Hello123", pattern=r"^[a-z]+$")
    
    with pytest.raises(ValueError, match="value does not match required pattern: \\^\\\\d\\+\\$"):
        validate_string("abc", pattern=r"^\d+$")
    
    # Test with compiled pattern
    compiled_pattern = re.compile(r"^[A-Z]+$")
    with pytest.raises(ValueError, match="value does not match required pattern: \\^\\[A-Z\\]\\+\\$"):
        validate_string("hello", pattern=compiled_pattern)


def test_validate_string_value_error_character_violations() -> None:
    """
    Test case 14: ValueError for character restriction violations.
    """
    # Test disallowed characters
    with pytest.raises(ValueError, match="value contains disallowed character: x"):
        validate_string("hello world", allowed_chars="helo wrd")
    
    # Test forbidden characters
    with pytest.raises(ValueError, match="value contains forbidden character: !"):
        validate_string("hello!", forbidden_chars="!@#$")
    
    with pytest.raises(ValueError, match="value contains forbidden character: @"):
        validate_string("user@domain", forbidden_chars="@")


def test_validate_string_edge_cases() -> None:
    """
    Test case 15: Edge cases and boundary conditions.
    """
    # Test single character strings
    validate_string("a", min_length=1, max_length=1)
    
    # Test very long strings
    long_string = "a" * 10000
    validate_string(long_string, max_length=20000)
    
    # Test unicode strings
    validate_string("héllo wörld", pattern=r"^[\w\s]+$")
    validate_string("你好", allowed_chars="你好")
    
    # Test strings with newlines and tabs
    validate_string("hello\nworld\t!", allowed_chars="helo wrldn!\t")
    
    # Test edge case: min_length > max_length (should be caught in parameter validation)
    with pytest.raises(ValueError, match="min_length \\(10\\) cannot be greater than max_length \\(5\\)"):
        validate_string("hello", min_length=10, max_length=5)


def test_validate_string_performance_large_strings() -> None:
    """
    Test case 16: Performance with large strings and complex patterns.
    """
    # Test large string validation
    large_string = "a" * 100000
    
    import time
    start_time = time.time()
    validate_string(large_string, min_length=50000, max_length=200000)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 0.1  # Should be fast for basic validation
    
    # Test pattern matching performance
    medium_string = "a" * 10000
    start_time = time.time()
    validate_string(medium_string, pattern=r"^a+$")
    elapsed_time = time.time() - start_time
    assert elapsed_time < 1.0  # Should complete within 1 second
