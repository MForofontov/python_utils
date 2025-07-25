import pytest
from strings_utility.join_strings import join_strings


def test_join_strings_default_delimiter() -> None:
    """
    Test the join_strings function with the default delimiter (space).
    """
    # Test case 1: Join a list of strings with default delimiter (space)
    assert (
        join_strings(["hello", "world"]) == "hello world"
    ), "Failed on default delimiter"


def test_join_strings_custom_delimiter() -> None:
    """
    Test the join_strings function with a custom delimiter.
    """
    # Test case 2: Join a list of strings with a custom delimiter
    assert (
        join_strings(["hello", "world"], delimiter=",") == "hello,world"
    ), "Failed on custom delimiter"


def test_join_strings_empty_delimiter() -> None:
    """
    Test the join_strings function with an empty delimiter.
    """
    # Test case 3: Join a list of strings with an empty delimiter
    assert (
        join_strings(["hello", "world"], delimiter="") == "helloworld"
    ), "Failed on empty delimiter"


def test_join_strings_single_string() -> None:
    """
    Test the join_strings function with a single string.
    """
    # Test case 4: Join a list of strings with a single string
    assert join_strings(["hello"]) == "hello", "Failed on single string"


def test_join_strings_empty_list() -> None:
    """
    Test the join_strings function with an empty list of strings.
    """
    # Test case 5: Join an empty list of strings
    assert join_strings([]) == "", "Failed on empty list"


def test_join_strings_special_characters() -> None:
    """
    Test the join_strings function with a list of strings that includes special characters.
    """
    # Test case 6: Join a list of strings with special characters
    assert (
        join_strings(["hello", "world!"], delimiter=" ") == "hello world!"
    ), "Failed on special characters"


def test_join_strings_numbers() -> None:
    """
    Test the join_strings function with a list of strings that includes numbers.
    """
    # Test case 7: Join a list of strings with numbers
    assert join_strings(["123", "456"], delimiter="-") == "123-456", "Failed on numbers"


def test_join_strings_mixed_case() -> None:
    """
    Test the join_strings function with a list of strings that includes mixed case.
    """
    # Test case 8: Join a list of strings with mixed case
    assert (
        join_strings(["Hello", "World"], delimiter=" ") == "Hello World"
    ), "Failed on mixed case"


def test_join_strings_leading_trailing_spaces() -> None:
    """
    Test the join_strings function with a list of strings that includes leading and trailing spaces.
    """
    # Test case 9: Join a list of strings with leading and trailing spaces
    assert (
        join_strings(["  hello", "world  "], delimiter=" ") == "  hello world  "
    ), "Failed on leading and trailing spaces"


def test_join_strings_newline_characters() -> None:
    """
    Test the join_strings function with a list of strings that includes newline characters.
    """
    # Test case 10: Join a list of strings with newline characters
    assert (
        join_strings(["hello", "world"], delimiter="\n") == "hello\nworld"
    ), "Failed on newline characters"


def test_join_strings_tab_characters() -> None:
    """
    Test the join_strings function with a list of strings that includes tab characters.
    """
    # Test case 11: Join a list of strings with tab characters
    assert (
        join_strings(["hello", "world"], delimiter="\t") == "hello\tworld"
    ), "Failed on tab characters"


def test_join_strings_mixed_whitespace_characters() -> None:
    """
    Test the join_strings function with a list of strings that includes mixed whitespace characters.
    """
    # Test case 12: Join a list of strings with mixed whitespace characters
    assert (
        join_strings(["hello", "world"], delimiter=" \t\n") == "hello \t\nworld"
    ), "Failed on mixed whitespace characters"


def test_join_strings_non_english_characters() -> None:
    """
    Test the join_strings function with a list of strings that includes non-English characters.
    """
    # Test case 13: Join a list of strings with non-English characters
    assert (
        join_strings(["héllo", "wörld"], delimiter=" ") == "héllo wörld"
    ), "Failed on non-English characters"


def test_join_strings_punctuation() -> None:
    """
    Test the join_strings function with a list of strings that includes punctuation.
    """
    # Test case 14: Join a list of strings with punctuation
    assert (
        join_strings(["hello,", "world!"], delimiter=" ") == "hello, world!"
    ), "Failed on punctuation"


def test_join_strings_mixed_alphanumeric() -> None:
    """
    Test the join_strings function with a list of strings that includes mixed alphanumeric characters.
    """
    # Test case 15: Join a list of strings with mixed alphanumeric characters
    assert (
        join_strings(["abc123", "456def"], delimiter=" ") == "abc123 456def"
    ), "Failed on mixed alphanumeric characters"


def test_join_strings_leading_trailing_delimiters() -> None:
    """
    Test the join_strings function with a list of strings that includes leading and trailing delimiters.
    """
    # Test case 16: Join a list of strings with leading and trailing delimiters
    assert (
        join_strings(["hello", "world"], delimiter=" ") == "hello world"
    ), "Failed on leading and trailing delimiters"


def test_join_strings_multiple_delimiters() -> None:
    """
    Test the join_strings function with a list of strings that includes multiple delimiters.
    """
    # Test case 17: Join a list of strings with multiple delimiters
    assert (
        join_strings(["hello", "world"], delimiter="---") == "hello---world"
    ), "Failed on multiple delimiters"


def test_join_strings_invalid_strings_type() -> None:
    """
    Test the join_strings function with an invalid strings type.
    """
    # Test case 18: Invalid strings type
    with pytest.raises(TypeError):
        join_strings("hello world", delimiter=" ")


def test_join_strings_invalid_delimiter_type() -> None:
    """
    Test the join_strings function with an invalid delimiter type.
    """
    # Test case 19: Invalid delimiter type
    with pytest.raises(TypeError):
        join_strings(["hello", "world"], delimiter=123)
