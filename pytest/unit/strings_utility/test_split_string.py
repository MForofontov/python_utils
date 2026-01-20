import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from pyutils_collection.strings_utility.split_string import split_string


def test_split_string_default_delimiter() -> None:
    """
    Test case 1: Test the split_string function with the default delimiter (space).
    """
    assert split_string("hello world") == [
        "hello",
        "world",
    ], "Failed on default delimiter"


def test_split_string_custom_delimiter() -> None:
    """
    Test case 2: Test the split_string function with a custom delimiter.
    """
    assert split_string("a,b,c", delimiter=",") == [
        "a",
        "b",
        "c",
    ], "Failed on custom delimiter"


def test_split_string_empty_string() -> None:
    """
    Test case 3: Test the split_string function with an empty string.
    """
    assert split_string("") == [""], "Failed on empty string"


def test_split_string_no_delimiter_in_string() -> None:
    """
    Test case 4: Test the split_string function when the delimiter is not in the string.
    """
    assert split_string("hello") == ["hello"], "Failed on no delimiter in the string"


def test_split_string_multiple_delimiters() -> None:
    """
    Test case 5: Test the split_string function with multiple delimiters in the string.
    """
    assert split_string("a,,b,,c", delimiter=",") == [
        "a",
        "",
        "b",
        "",
        "c",
    ], "Failed on multiple delimiters"


def test_split_string_leading_trailing_delimiters() -> None:
    """
    Test case 6: Test the split_string function with leading and trailing delimiters.
    """
    assert split_string(",a,b,c,", delimiter=",") == [
        "",
        "a",
        "b",
        "c",
        "",
    ], "Failed on leading and trailing delimiters"


def test_split_string_special_characters() -> None:
    """
    Test case 7: Test the split_string function with special characters as delimiters.
    """
    assert split_string("a!b!c", delimiter="!") == [
        "a",
        "b",
        "c",
    ], "Failed on special characters as delimiters"


def test_split_string_numbers() -> None:
    """
    Test case 8: Test the split_string function with numbers as delimiters.
    """
    assert split_string("1a2b3c", delimiter="2") == [
        "1a",
        "b3c",
    ], "Failed on numbers as delimiters"


def test_split_string_mixed_case() -> None:
    """
    Test case 9: Test the split_string function with mixed case letters.
    """
    assert split_string("HelloWorld", delimiter="W") == [
        "Hello",
        "orld",
    ], "Failed on mixed case letters"


def test_split_string_non_english_characters() -> None:
    """
    Test case 10: Test the split_string function with non-English characters.
    """
    assert split_string("héllo wörld", delimiter=" ") == [
        "héllo",
        "wörld",
    ], "Failed on non-English characters"


def test_split_string_mixed_whitespace() -> None:
    """
    Test case 11: Test the split_string function with mixed whitespace characters.
    """
    assert split_string("hello\tworld\nhello", delimiter="\t") == [
        "hello",
        "world\nhello",
    ], "Failed on mixed whitespace characters"


def test_split_string_empty_delimiter() -> None:
    """
    Test case 12: Test the split_string function with an empty delimiter.
    """
    with pytest.raises(ValueError):
        split_string("hello world", delimiter="")


def test_split_string_invalid_string_type() -> None:
    """
    Test case 13: Test the split_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        split_string(12345)


def test_split_string_invalid_delimiter_type() -> None:
    """
    Test case 14: Test the split_string function with an invalid delimiter type.
    """
    with pytest.raises(TypeError):
        split_string("hello world", delimiter=123)
