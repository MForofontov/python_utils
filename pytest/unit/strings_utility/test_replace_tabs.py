import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from pyutils_collection.strings_utility.replace_tabs import replace_tabs


def test_replace_tabs_default_tabsize() -> None:
    """
    Test case 1: Test the replace_tabs function with the default tab size (4 spaces).
    """
    assert replace_tabs("hello\tworld") == "hello    world", (
        "Failed on default tab size"
    )


def test_replace_tabs_custom_tabsize() -> None:
    """
    Test case 2: Test the replace_tabs function with a custom tab size.
    """
    assert replace_tabs("hello\tworld", 8) == "hello        world", (
        "Failed on custom tab size"
    )


def test_replace_tabs_multiple_tabs() -> None:
    """
    Test case 3: Test the replace_tabs function with a string that contains multiple tabs.
    """
    assert replace_tabs("hello\tworld\t!") == "hello    world    !", (
        "Failed on string with multiple tabs"
    )


def test_replace_tabs_tabs_and_spaces() -> None:
    """
    Test case 4: Test the replace_tabs function with a string that contains both tabs and spaces.
    """
    assert replace_tabs("hello \t world") == "hello      world", (
        "Failed on string with both tabs and spaces"
    )


def test_replace_tabs_empty_string() -> None:
    """
    Test case 5: Test the replace_tabs function with an empty string.
    """
    assert replace_tabs("") == "", "Failed on empty string"


def test_replace_tabs_no_tabs() -> None:
    """
    Test case 6: Test the replace_tabs function with a string that contains no tabs.
    """
    assert replace_tabs("hello world") == "hello world", "Failed on string with no tabs"


def test_replace_tabs_special_characters() -> None:
    """
    Test case 7: Test the replace_tabs function with a string that contains special characters.
    """
    assert replace_tabs("hello\t!@#") == "hello    !@#", (
        "Failed on string with special characters"
    )


def test_replace_tabs_numbers_and_letters() -> None:
    """
    Test case 8: Test the replace_tabs function with a string that contains both numbers and letters.
    """
    assert replace_tabs("abc123\txyz") == "abc123    xyz", (
        "Failed on string with numbers and letters"
    )


def test_replace_tabs_non_english_characters() -> None:
    """
    Test case 9: Test the replace_tabs function with a string that contains non-English characters.
    """
    assert replace_tabs("héllo\twörld") == "héllo    wörld", (
        "Failed on string with non-English characters"
    )


def test_replace_tabs_mixed_whitespace() -> None:
    """
    Test case 10: Test the replace_tabs function with a string that contains mixed whitespace characters.
    """
    assert replace_tabs(" \t\nhello\tworld\t\n ") == "     \nhello    world    \n ", (
        "Failed on string with mixed whitespace characters"
    )


def test_replace_tabs_tabs_non_english_characters() -> None:
    """
    Test case 11: Test the replace_tabs function with a string that contains tabs and non-English characters.
    """
    assert replace_tabs("héllo\twörld") == "héllo    wörld", (
        "Failed on string with tabs and non-English characters"
    )


def test_replace_tabs_tabs_leading_spaces() -> None:
    """
    Test case 12: Test the replace_tabs function with a string that contains tabs and leading spaces.
    """
    assert replace_tabs("    \thello") == "        hello", (
        "Failed on string with tabs and leading spaces"
    )


def test_replace_tabs_tabs_trailing_spaces() -> None:
    """
    Test case 13: Test the replace_tabs function with a string that contains tabs and trailing spaces.
    """
    assert replace_tabs("hello\t    ") == "hello        ", (
        "Failed on string with tabs and trailing spaces"
    )


def test_replace_tabs_invalid_string_type() -> None:
    """
    Test case 14: Test the replace_tabs function with an invalid string type.
    """
    with pytest.raises(TypeError):
        replace_tabs(12345)


def test_replace_tabs_invalid_tabsize_type() -> None:
    """
    Test case 15: Test the replace_tabs function with an invalid tab size type.
    """
    with pytest.raises(TypeError):
        replace_tabs("hello\tworld", "4")


def test_replace_tabs_negative_tabsize() -> None:
    """
    Test case 16: Test the replace_tabs function with a negative tab size.
    """
    with pytest.raises(ValueError):
        replace_tabs("hello\tworld", -4)
