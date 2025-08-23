import pytest
from strings_utility.verify_password import verify_password


def test_verify_password_valid() -> None:
    """
    Test the verify_password function with a valid password.
    """
    # Test case 1: Valid password
    assert verify_password("Password123!") == True, "Failed on valid password"


def test_verify_password_too_short() -> None:
    """
    Test the verify_password function with a password that is too short.
    """
    # Test case 2: Password too short
    assert verify_password("Pass1!") == False, "Failed on password too short"


def test_verify_password_no_uppercase() -> None:
    """
    Test the verify_password function with a password that has no uppercase characters.
    """
    # Test case 3: No uppercase characters
    assert verify_password(
        "password123!") == False, "Failed on no uppercase characters"


def test_verify_password_no_lowercase() -> None:
    """
    Test the verify_password function with a password that has no lowercase characters.
    """
    # Test case 4: No lowercase characters
    assert verify_password(
        "PASSWORD123!") == False, "Failed on no lowercase characters"


def test_verify_password_no_digits() -> None:
    """
    Test the verify_password function with a password that has no numerical digits.
    """
    # Test case 5: No numerical digits
    assert verify_password(
        "Password!!!") == False, "Failed on no numerical digits"


def test_verify_password_no_special_characters() -> None:
    """
    Test the verify_password function with a password that has no special characters.
    """
    # Test case 6: No special characters
    assert verify_password(
        "Password123") == False, "Failed on no special characters"


def test_verify_password_empty_string() -> None:
    """
    Test the verify_password function with an empty string.
    """
    # Test case 7: Empty string
    assert verify_password("") == False, "Failed on empty string"


def test_verify_password_custom_check_pass() -> None:
    """
    Test the verify_password function with a custom check that passes.
    """
    # Test case 8: Custom check that passes
    def custom_check(p): return "example" in p
    assert (
        verify_password("Password123!example",
                        custom_checks=[custom_check]) == True
    ), "Failed on custom check that passes"


def test_verify_password_custom_check_fail() -> None:
    """
    Test the verify_password function with a custom check that fails.
    """
    # Test case 9: Custom check that fails
    def custom_check(p): return "example" in p
    assert (
        verify_password("Password123!", custom_checks=[custom_check]) == False
    ), "Failed on custom check that fails"


def test_verify_password_no_shared_state() -> None:
    """
    Test that repeated calls do not share state between invocations.
    """
    # Test case 10: Ensure no shared state between calls
    calls: list[str] = []

    def custom_check(p: str) -> bool:
        calls.append(p)
        return True

    assert verify_password("Password123!", custom_checks=[custom_check])
    assert calls == ["Password123!"]

    assert verify_password("Password123!")
    assert calls == ["Password123!"]


def test_verify_password_invalid_type() -> None:
    """
    Test the verify_password function with an invalid type.
    """
    # Test case 11: Invalid type
    with pytest.raises(TypeError):
        verify_password(12345)
