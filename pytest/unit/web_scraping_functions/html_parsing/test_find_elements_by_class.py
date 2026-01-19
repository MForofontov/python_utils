import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from web_scraping_functions.html_parsing.find_elements_by_class import (
        find_elements_by_class,
    )
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    find_elements_by_class = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")


def test_find_elements_by_class_single_class() -> None:
    """
    Test case 1: Find elements by single class.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_class(soup, "item")

    # Assert
    assert len(result) == 2
    assert result[0].text == "A"
    assert result[1].text == "B"


def test_find_elements_by_class_with_limit() -> None:
    """
    Test case 2: Find elements with limit.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div><div class="item">C</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_class(soup, "item", limit=2)

    # Assert
    assert len(result) == 2


def test_find_elements_by_class_no_matches() -> None:
    """
    Test case 3: Find elements with no matches.
    """
    # Arrange
    html = '<div class="other">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_class(soup, "item")

    # Assert
    assert result == []


def test_find_elements_by_class_nested_elements() -> None:
    """
    Test case 4: Find nested elements by class.
    """
    # Arrange
    html = '<div class="outer"><div class="inner">Content</div></div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_class(soup, "inner")

    # Assert
    assert len(result) == 1
    assert result[0].text == "Content"


def test_find_elements_by_class_multiple_classes() -> None:
    """
    Test case 5: Find elements with multiple classes on same element.
    """
    # Arrange
    html = '<div class="item active">A</div><div class="item">B</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_class(soup, "item")

    # Assert
    assert len(result) == 2


def test_find_elements_by_class_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        find_elements_by_class("not a soup", "item")


def test_find_elements_by_class_type_error_class_name() -> None:
    """
    Test case 7: TypeError for invalid class_name type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="class_name must be a string"):
        find_elements_by_class(soup, 123)


def test_find_elements_by_class_type_error_limit() -> None:
    """
    Test case 8: TypeError for invalid limit type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="limit must be an integer or None"):
        find_elements_by_class(soup, "item", limit="5")


def test_find_elements_by_class_value_error_empty_class_name() -> None:
    """
    Test case 9: ValueError for empty class_name.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="class_name cannot be empty"):
        find_elements_by_class(soup, "")


def test_find_elements_by_class_value_error_negative_limit() -> None:
    """
    Test case 10: ValueError for non-positive limit.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="limit must be positive"):
        find_elements_by_class(soup, "item", limit=0)
