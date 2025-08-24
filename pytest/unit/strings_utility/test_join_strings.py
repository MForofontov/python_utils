import pytest
from strings_utility.join_strings import join_strings


def test_join_strings_default_delimiter() -> None:
    """
    Test case 1: Test the join_strings function with the default delimiter (space).
    """
    assert (
        join_strings(["hello", "world"]) == "hello world"
    ), "Failed on default delimiter"


def test_join_strings_custom_delimiter() -> None:
    """
    Test case 2: Test the join_strings function with a custom delimiter.
    """
    assert (
        join_strings(["hello", "world"], delimiter=",") == "hello,world"
    ), "Failed on custom delimiter"


def test_join_strings_empty_delimiter() -> None:
    """
    Test case 3: Test the join_strings function with an empty delimiter.
    """
    assert (
        join_strings(["hello", "world"], delimiter="") == "helloworld"
    ), "Failed on empty delimiter"


def test_join_strings_single_string() -> None:
    """
    Test case 4: Test the join_strings function with a single string.
    """
    assert join_strings(["hello"]) == "hello", "Failed on single string"


def test_join_strings_empty_list() -> None:
    """
    Test case 5: Test the join_strings function with an empty list of strings.
    """
    assert join_strings([]) == "", "Failed on empty list"


def test_join_strings_special_characters() -> None:
    """
    Test case 6: Test the join_strings function with a list of strings that includes special characters.
    """
    assert (
        join_strings(["hello", "world!"], delimiter=" ") == "hello world!"
    ), "Failed on special characters"


def test_join_strings_numbers() -> None:
    """
    Test case 7: Test the join_strings function with a list of strings that includes numbers.
    """
    assert join_strings(
        ["123", "456"], delimiter="-") == "123-456", "Failed on numbers"


def test_join_strings_mixed_case() -> None:
    """
    Test case 8: Test the join_strings function with a list of strings that includes mixed case.
    """
    assert (
        join_strings(["Hello", "World"], delimiter=" ") == "Hello World"
    ), "Failed on mixed case"


def test_join_strings_leading_trailing_spaces() -> None:
    """
    Test case 9: Test the join_strings function with a list of strings that includes leading and trailing spaces.
    """
    assert (
        join_strings(["  hello", "world  "],
                     delimiter=" ") == "  hello world  "
    ), "Failed on leading and trailing spaces"


def test_join_strings_newline_characters() -> None:
    """
    Test case 10: Test the join_strings function with a list of strings that includes newline characters.
    """
    assert (
        join_strings(["hello", "world"], delimiter="\n") == "hello\nworld"
    ), "Failed on newline characters"


def test_join_strings_tab_characters() -> None:
    """
    Test case 11: Test the join_strings function with a list of strings that includes tab characters.
    """
    assert (
        join_strings(["hello", "world"], delimiter="\t") == "hello\tworld"
    ), "Failed on tab characters"


def test_join_strings_mixed_whitespace_characters() -> None:
    """
    Test case 12: Test the join_strings function with a list of strings that includes mixed whitespace characters.
    """
    assert (
        join_strings(["hello", "world"],
                     delimiter=" \t\n") == "hello \t\nworld"
    ), "Failed on mixed whitespace characters"


def test_join_strings_non_english_characters() -> None:
    """
    Test case 13: Test the join_strings function with a list of strings that includes non-English characters.
    """
    assert (
        join_strings(["héllo", "wörld"], delimiter=" ") == "héllo wörld"
    ), "Failed on non-English characters"


def test_join_strings_punctuation() -> None:
    """
    Test case 14: Test the join_strings function with a list of strings that includes punctuation.
    """
    assert (
        join_strings(["hello,", "world!"], delimiter=" ") == "hello, world!"
    ), "Failed on punctuation"


def test_join_strings_mixed_alphanumeric() -> None:
    """
    Test case 15: Test the join_strings function with a list of strings that includes mixed alphanumeric characters.
    """
    assert (
        join_strings(["abc123", "456def"], delimiter=" ") == "abc123 456def"
    ), "Failed on mixed alphanumeric characters"


def test_join_strings_leading_trailing_delimiters() -> None:
    """
    Test case 16: Test the join_strings function with a list of strings that includes leading and trailing delimiters.
    """
    assert (
        join_strings(["hello", "world"], delimiter=" ") == "hello world"
    ), "Failed on leading and trailing delimiters"


def test_join_strings_multiple_delimiters() -> None:
    """
    Test case 17: Test the join_strings function with a list of strings that includes multiple delimiters.
    """
    assert (
        join_strings(["hello", "world"], delimiter="---") == "hello---world"
    ), "Failed on multiple delimiters"


def test_join_strings_invalid_strings_type() -> None:
    """
    Test case 18: Test the join_strings function with an invalid strings type.
    """
    with pytest.raises(TypeError):
        join_strings("hello world", delimiter=" ")


def test_join_strings_invalid_delimiter_type() -> None:
    """
    Test case 19: Test the join_strings function with an invalid delimiter type.
    """
    with pytest.raises(TypeError):
        join_strings(["hello", "world"], delimiter=123)
