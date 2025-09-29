"""
Unit tests for validate_email function.

This module contains comprehensive tests for the validate_email function,
including format validation, Unicode support, and domain checking.
"""

from unittest.mock import patch

import pytest
from data_validation import validate_email


def test_validate_email_case_1_valid_emails() -> None:
    """
    Test case 1: Valid email address formats.
    """
    # Test basic valid emails
    validate_email("user@example.com")
    validate_email("test@domain.org")
    validate_email("admin@company.net")

    # Test complex valid emails
    validate_email("user.name@example.com")
    validate_email("user+tag@example.com")
    validate_email("user_123@example-domain.com")
    validate_email("first.last+tag@subdomain.example.co.uk")


def test_validate_email_case_2_subdomain_and_tld_variations() -> None:
    """
    Test case 2: Valid emails with various subdomain and TLD combinations.
    """
    # Test subdomains
    validate_email("user@mail.example.com")
    validate_email("user@sub.domain.example.org")

    # Test various TLDs
    validate_email("user@example.co.uk")
    validate_email("user@example.info")
    validate_email("user@example.museum")
    validate_email("user@example.travel")


def test_validate_email_case_3_unicode_emails() -> None:
    """
    Test case 3: Unicode email addresses when allowed.
    """
    # Test Unicode emails with allow_unicode=True
    validate_email("тест@example.com", allow_unicode=True)
    validate_email("用户@example.com", allow_unicode=True)
    validate_email("user@üñíçøðé.com", allow_unicode=True)


def test_validate_email_case_4_edge_case_valid_emails() -> None:
    """
    Test case 4: Edge cases that should be valid.
    """
    # Test minimum length email
    validate_email("a@b.co")

    # Test numbers in local part
    validate_email("123@example.com")
    validate_email("user123@example.com")

    # Test hyphens in domain
    validate_email("user@test-domain.com")
    validate_email("user@sub-domain.example-site.org")


def test_validate_email_case_5_type_error_invalid_input() -> None:
    """
    Test case 5: TypeError for non-string input.
    """
    with pytest.raises(TypeError, match="email must be str, got int"):
        validate_email(123)

    with pytest.raises(TypeError, match="email must be str, got list"):
        validate_email(["user@example.com"])

    with pytest.raises(TypeError, match="email must be str, got NoneType"):
        validate_email(None)

    # Test with custom param name
    with pytest.raises(TypeError, match="user_email must be str, got int"):
        validate_email(123, param_name="user_email")


def test_validate_email_case_6_type_error_invalid_parameters() -> None:
    """
    Test case 6: TypeError for invalid parameter types.
    """
    with pytest.raises(TypeError, match="allow_unicode must be bool, got str"):
        validate_email("user@example.com", allow_unicode="true")

    with pytest.raises(TypeError, match="check_mx must be bool, got int"):
        validate_email("user@example.com", check_mx=1)

    with pytest.raises(TypeError, match="param_name must be str, got int"):
        validate_email("user@example.com", param_name=123)


def test_validate_email_case_7_value_error_empty_email() -> None:
    """
    Test case 7: ValueError for empty email addresses.
    """
    with pytest.raises(ValueError, match="email cannot be empty"):
        validate_email("")

    # Test with custom param name
    with pytest.raises(ValueError, match="user_email cannot be empty"):
        validate_email("", param_name="user_email")


def test_validate_email_case_8_value_error_length_violations() -> None:
    """
    Test case 8: ValueError for length constraint violations.
    """
    # Test email too long (over 254 characters)
    long_email = "a" * 250 + "@example.com"
    with pytest.raises(
        ValueError, match="email exceeds maximum length of 254 characters"
    ):
        validate_email(long_email)

    # Test local part too long (over 64 characters)
    long_local = "a" * 65 + "@example.com"
    with pytest.raises(
        ValueError, match="email local part exceeds maximum length of 64 characters"
    ):
        validate_email(long_local)

    # Test domain part too long (over 253 characters)
    long_domain = "user@" + "a" * 250 + ".com"
    with pytest.raises(
        ValueError, match="email exceeds maximum length of 254 characters"
    ):
        validate_email(long_domain)


def test_validate_email_case_9_value_error_invalid_structure() -> None:
    """
    Test case 9: ValueError for invalid email structure.
    """
    # Test missing @ symbol
    with pytest.raises(ValueError, match="email must contain exactly one @ symbol"):
        validate_email("userexample.com")

    # Test multiple @ symbols
    with pytest.raises(ValueError, match="email must contain exactly one @ symbol"):
        validate_email("user@@example.com")

    with pytest.raises(ValueError, match="email must contain exactly one @ symbol"):
        validate_email("user@example@.com")

    # Test empty local part
    with pytest.raises(ValueError, match="email local part cannot be empty"):
        validate_email("@example.com")

    # Test empty domain part
    with pytest.raises(ValueError, match="email domain part cannot be empty"):
        validate_email("user@")


def test_validate_email_case_10_value_error_invalid_format() -> None:
    """
    Test case 10: ValueError for invalid email format.
    """
    # Test invalid local part format
    with pytest.raises(ValueError, match="email local part format is invalid"):
        validate_email("user..name@example.com")  # consecutive dots

    with pytest.raises(ValueError, match="email local part format is invalid"):
        validate_email(".user@example.com")  # starts with dot

    with pytest.raises(ValueError, match="email local part format is invalid"):
        validate_email("user.@example.com")  # ends with dot

    # Test invalid domain format
    with pytest.raises(ValueError, match="email domain cannot start or end with a dot"):
        validate_email("user@.example.com")  # starts with dot

    with pytest.raises(ValueError, match="email domain cannot start or end with a dot"):
        validate_email("user@example.com.")  # ends with dot

    with pytest.raises(
        ValueError, match="email domain cannot contain consecutive dots"
    ):
        validate_email("user@example..com")


def test_validate_email_case_11_value_error_domain_requirements() -> None:
    """
    Test case 11: ValueError for domain requirement violations.
    """
    # Test domain without TLD
    with pytest.raises(ValueError, match="email domain must contain at least one dot"):
        validate_email("user@localhost")

    with pytest.raises(ValueError, match="email domain must contain at least one dot"):
        validate_email("user@domain")


def test_validate_email_case_12_value_error_unicode_not_allowed() -> None:
    """
    Test case 12: ValueError for Unicode characters when not allowed.
    """
    with pytest.raises(
        ValueError, match="email contains non-ASCII characters but allow_unicode=False"
    ):
        validate_email("тест@example.com", allow_unicode=False)

    with pytest.raises(
        ValueError, match="email contains non-ASCII characters but allow_unicode=False"
    ):
        validate_email("user@üñíçøðé.com", allow_unicode=False)

    with pytest.raises(
        ValueError, match="email contains non-ASCII characters but allow_unicode=False"
    ):
        validate_email("用户@example.com")  # default allow_unicode=False


@patch("socket.gethostbyname")
def test_validate_email_case_13_mx_checking_success(mock_gethostbyname) -> None:
    """
    Test case 13: Successful MX record checking.
    """
    # Mock successful domain resolution
    mock_gethostbyname.return_value = "1.2.3.4"

    # Test with check_mx=True (fallback to A record)
    validate_email("user@example.com", check_mx=True)
    mock_gethostbyname.assert_called_with("example.com")


@patch("socket.gethostbyname")
def test_validate_email_case_14_mx_checking_failure(mock_gethostbyname) -> None:
    """
    Test case 14: Failed MX record checking.
    """
    import socket

    # Mock failed domain resolution
    mock_gethostbyname.side_effect = socket.gaierror("Name resolution failed")

    # Test with check_mx=True
    with pytest.raises(ValueError, match="email domain does not exist"):
        validate_email("user@nonexistent-domain-12345.com", check_mx=True)


def test_validate_email_case_15_edge_cases() -> None:
    """
    Test case 15: Edge cases and boundary conditions.
    """
    # Test minimum valid email
    validate_email("a@b.co")

    # Test maximum local part length (64 characters)
    max_local = "a" * 64 + "@example.com"
    validate_email(max_local)

    # Test complex but valid emails
    validate_email("test.email.with+symbol@example-domain.co.uk")
    validate_email("user123+tag456@sub.domain.example.org")

    # Test numbers and hyphens
    validate_email("123@456-789.com")
    validate_email("user-name@domain-name.org")


def test_validate_email_case_16_performance_complex_emails() -> None:
    """
    Test case 16: Performance with complex email validation.
    """
    # Test performance with many validations
    emails = [
        "user1@example.com",
        "user2@domain.org",
        "test.email@subdomain.example.co.uk",
        "complex+tag@test-domain.info",
    ]

    import time

    start_time = time.time()
    for _ in range(1000):
        for email in emails:
            validate_email(email)
    elapsed_time = time.time() - start_time

    assert elapsed_time < 1.0  # Should complete within 1 second
