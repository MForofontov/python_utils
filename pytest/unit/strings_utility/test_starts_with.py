import pytest
from strings_utility.starts_with import starts_with


def test_starts_with_basic_true() -> None:
    """
    Test case 1: Test the starts_with function with a basic case where the string starts with the prefix.
    """
    assert starts_with(
        "hello world", "hello") == True, "Failed on basic true case"


def test_starts_with_basic_false() -> None:
    """
    Test case 2: Test the starts_with function with a basic case where the string does not start with the prefix.
    """
    assert starts_with(
        "hello world", "world") == False, "Failed on basic false case"


def test_starts_with_empty_string() -> None:
    """
    Test case 3: Test the starts_with function with an empty string.
    """
    assert starts_with("", "hello") == False, "Failed on empty string"


def test_starts_with_empty_prefix() -> None:
    """
    Test case 4: Test the starts_with function with an empty prefix.
    """
    assert starts_with("hello world", "") == True, "Failed on empty prefix"


def test_starts_with_both_empty() -> None:
    """
    Test case 5: Test the starts_with function with both the string and the prefix being empty.
    """
    assert starts_with(
        "", "") == True, "Failed on both string and prefix being empty"


def test_starts_with_special_characters() -> None:
    """
    Test case 6: Test the starts_with function with special characters.
    """
    assert starts_with(
        "!@#hello", "!@#") == True, "Failed on special characters"


def test_starts_with_numbers() -> None:
    """
    Test case 7: Test the starts_with function with numbers.
    """
    assert starts_with("12345hello", "12345") == True, "Failed on numbers"


def test_starts_with_mixed_case_true() -> None:
    """
    Test case 8: Test the starts_with function with mixed case where the string starts with the prefix.
    """
    assert starts_with(
        "HelloWorld", "Hello") == True, "Failed on mixed case true"


def test_starts_with_mixed_case_false() -> None:
    """
    Test case 9: Test the starts_with function with mixed case where the string does not start with the prefix.
    """
    assert starts_with(
        "HelloWorld", "hello") == False, "Failed on mixed case false"


def test_starts_with_non_english_characters() -> None:
    """
    Test case 10: Test the starts_with function with non-English characters.
    """
    assert (
        starts_with("héllo wörld", "héllo") == True
    ), "Failed on non-English characters"


def test_starts_with_whitespace_characters() -> None:
    """
    Test case 11: Test the starts_with function with whitespace characters.
    """
    assert starts_with(
        "   hello", "   ") == True, "Failed on whitespace characters"


def test_starts_with_newline_characters() -> None:
    """
    Test case 12: Test the starts_with function with newline characters.
    """
    assert starts_with("\nhello", "\n") == True, "Failed on newline characters"


def test_starts_with_tab_characters() -> None:
    """
    Test case 13: Test the starts_with function with tab characters.
    """
    assert starts_with("\thello", "\t") == True, "Failed on tab characters"


def test_starts_with_mixed_whitespace_characters() -> None:
    """
    Test case 14: Test the starts_with function with mixed whitespace characters.
    """
    assert (
        starts_with(" \t\nhello", " \t\n") == True
    ), "Failed on mixed whitespace characters"


def test_starts_with_invalid_string_type() -> None:
    """
    Test case 15: Test the starts_with function with an invalid string type.
    """
    with pytest.raises(TypeError):
        starts_with(12345, "hello")


def test_starts_with_invalid_prefix_type() -> None:
    """
    Test case 16: Test the starts_with function with an invalid prefix type.
    """
    with pytest.raises(TypeError):
        starts_with("hello world", 123)
