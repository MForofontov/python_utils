import pytest
from strings_utility.remove_non_alphanumeric import remove_non_alphanumeric


def test_remove_non_alphanumeric_mixed_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains both alphanumeric and non-alphanumeric characters.
    """
    # Test case 1: String with mixed alphanumeric and non-alphanumeric characters
    assert (
        remove_non_alphanumeric("abc123!@#") == "abc123"
    ), "Failed on mixed alphanumeric and non-alphanumeric characters"


def test_remove_non_alphanumeric_only_alphanumeric() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains only alphanumeric characters.
    """
    # Test case 2: String with only alphanumeric characters
    assert (
        remove_non_alphanumeric("abc123") == "abc123"
    ), "Failed on string with only alphanumeric characters"


def test_remove_non_alphanumeric_only_non_alphanumeric() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains only non-alphanumeric characters.
    """
    # Test case 3: String with only non-alphanumeric characters
    assert (
        remove_non_alphanumeric("!@#$%^&*()") == ""
    ), "Failed on string with only non-alphanumeric characters"


def test_remove_non_alphanumeric_empty_string() -> None:
    """
    Test the remove_non_alphanumeric function with an empty string.
    """
    # Test case 4: Empty string
    assert remove_non_alphanumeric("") == "", "Failed on empty string"


def test_remove_non_alphanumeric_whitespace_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains whitespace characters.
    """
    # Test case 5: String with whitespace characters
    assert (
        remove_non_alphanumeric("abc 123 def") == "abc123def"
    ), "Failed on string with whitespace characters"


def test_remove_non_alphanumeric_newline_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains newline characters.
    """
    # Test case 6: String with newline characters
    assert (
        remove_non_alphanumeric("abc\n123\ndef") == "abc123def"
    ), "Failed on string with newline characters"


def test_remove_non_alphanumeric_tab_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains tab characters.
    """
    # Test case 7: String with tab characters
    assert (
        remove_non_alphanumeric("abc\t123\tdef") == "abc123def"
    ), "Failed on string with tab characters"


def test_remove_non_alphanumeric_mixed_whitespace_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains mixed whitespace characters.
    """
    # Test case 8: String with mixed whitespace characters
    assert (
        remove_non_alphanumeric("abc \t\n123 \t\ndef") == "abc123def"
    ), "Failed on string with mixed whitespace characters"


def test_remove_non_alphanumeric_leading_trailing_spaces() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains leading and trailing spaces.
    """
    # Test case 9: String with leading and trailing spaces
    assert (
        remove_non_alphanumeric(" 123 abc 456 ") == "123abc456"
    ), "Failed on string with leading and trailing spaces"


def test_remove_non_alphanumeric_non_english_characters() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains non-English characters.
    """
    # Test case 10: String with non-English characters
    assert (
        remove_non_alphanumeric("héllo123 wörld456") == "héllo123wörld456"
    ), "Failed on string with non-English characters"


def test_remove_non_alphanumeric_mixed_case() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains mixed case letters.
    """
    # Test case 11: String with mixed case letters
    assert (
        remove_non_alphanumeric("AbC123dEf456") == "AbC123dEf456"
    ), "Failed on string with mixed case letters"


def test_remove_non_alphanumeric_numbers_within_words() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains numbers within words.
    """
    # Test case 12: String with numbers within words
    assert (
        remove_non_alphanumeric("a1b2c3") == "a1b2c3"
    ), "Failed on string with numbers within words"


def test_remove_non_alphanumeric_numbers_at_start_and_end() -> None:
    """
    Test the remove_non_alphanumeric function with a string that contains numbers at the start and end.
    """
    # Test case 13: String with numbers at the start and end
    assert (
        remove_non_alphanumeric("123abc456") == "123abc456"
    ), "Failed on string with numbers at the start and end"


def test_remove_non_alphanumeric_invalid_type() -> None:
    """
    Test the remove_non_alphanumeric function with an invalid type.
    """
    # Test case 14: Invalid type
    with pytest.raises(TypeError):
        remove_non_alphanumeric(123)
