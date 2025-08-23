import pytest
from strings_utility.replace_tabs import replace_tabs


def test_replace_tabs_default_tabsize() -> None:
    """
    Test the replace_tabs function with the default tab size (4 spaces).
    """
    # Test case 1: Default tab size (4 spaces)
    assert (
        replace_tabs("hello\tworld") == "hello    world"
    ), "Failed on default tab size"


def test_replace_tabs_custom_tabsize() -> None:
    """
    Test the replace_tabs function with a custom tab size.
    """
    # Test case 2: Custom tab size
    assert (
        replace_tabs("hello\tworld", 8) == "hello        world"
    ), "Failed on custom tab size"


def test_replace_tabs_multiple_tabs() -> None:
    """
    Test the replace_tabs function with a string that contains multiple tabs.
    """
    # Test case 3: String with multiple tabs
    assert (
        replace_tabs("hello\tworld\t!") == "hello    world    !"
    ), "Failed on string with multiple tabs"


def test_replace_tabs_tabs_and_spaces() -> None:
    """
    Test the replace_tabs function with a string that contains both tabs and spaces.
    """
    # Test case 4: String with both tabs and spaces
    assert (
        replace_tabs("hello \t world") == "hello      world"
    ), "Failed on string with both tabs and spaces"


def test_replace_tabs_empty_string() -> None:
    """
    Test the replace_tabs function with an empty string.
    """
    # Test case 5: Empty string
    assert replace_tabs("") == "", "Failed on empty string"


def test_replace_tabs_no_tabs() -> None:
    """
    Test the replace_tabs function with a string that contains no tabs.
    """
    # Test case 6: String with no tabs
    assert replace_tabs(
        "hello world") == "hello world", "Failed on string with no tabs"


def test_replace_tabs_special_characters() -> None:
    """
    Test the replace_tabs function with a string that contains special characters.
    """
    # Test case 7: String with special characters
    assert (
        replace_tabs("hello\t!@#") == "hello    !@#"
    ), "Failed on string with special characters"


def test_replace_tabs_numbers_and_letters() -> None:
    """
    Test the replace_tabs function with a string that contains both numbers and letters.
    """
    # Test case 8: String with numbers and letters
    assert (
        replace_tabs("abc123\txyz") == "abc123    xyz"
    ), "Failed on string with numbers and letters"


def test_replace_tabs_non_english_characters() -> None:
    """
    Test the replace_tabs function with a string that contains non-English characters.
    """
    # Test case 9: String with non-English characters
    assert (
        replace_tabs("héllo\twörld") == "héllo    wörld"
    ), "Failed on string with non-English characters"


def test_replace_tabs_mixed_whitespace() -> None:
    """
    Test the replace_tabs function with a string that contains mixed whitespace characters.
    """
    # Test case 10: String with mixed whitespace characters
    assert (
        replace_tabs(
            " \t\nhello\tworld\t\n ") == "     \nhello    world    \n "
    ), "Failed on string with mixed whitespace characters"


def test_replace_tabs_tabs_non_english_characters() -> None:
    """
    Test the replace_tabs function with a string that contains tabs and non-English characters.
    """
    # Test case 11: String with tabs and non-English characters
    assert (
        replace_tabs("héllo\twörld") == "héllo    wörld"
    ), "Failed on string with tabs and non-English characters"


def test_replace_tabs_tabs_leading_spaces() -> None:
    """
    Test the replace_tabs function with a string that contains tabs and leading spaces.
    """
    # Test case 12: String with tabs and leading spaces
    assert (
        replace_tabs("    \thello") == "        hello"
    ), "Failed on string with tabs and leading spaces"


def test_replace_tabs_tabs_trailing_spaces() -> None:
    """
    Test the replace_tabs function with a string that contains tabs and trailing spaces.
    """
    # Test case 13: String with tabs and trailing spaces
    assert (
        replace_tabs("hello\t    ") == "hello        "
    ), "Failed on string with tabs and trailing spaces"


def test_replace_tabs_invalid_string_type() -> None:
    """
    Test the replace_tabs function with an invalid string type.
    """
    # Test case 14: Invalid string type
    with pytest.raises(TypeError):
        replace_tabs(12345)


def test_replace_tabs_invalid_tabsize_type() -> None:
    """
    Test the replace_tabs function with an invalid tab size type.
    """
    # Test case 15: Invalid tab size type
    with pytest.raises(TypeError):
        replace_tabs("hello\tworld", "4")


def test_replace_tabs_negative_tabsize() -> None:
    """
    Test the replace_tabs function with a negative tab size.
    """
    # Test case 16: Negative tab size
    with pytest.raises(ValueError):
        replace_tabs("hello\tworld", -4)
