import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from python_utils.web_scraping_functions.html_parsing.find_elements_by_id import (
        find_elements_by_id,
    )
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    find_elements_by_id = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_find_elements_by_id_simple_id() -> None:
    """
    Test case 1: Find element by ID.
    """
    # Arrange
    html = '<div id="main">Content</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_id(soup, "main")

    # Assert
    assert result is not None
    assert result.text == "Content"


def test_find_elements_by_id_no_match() -> None:
    """
    Test case 2: Return None when ID not found.
    """
    # Arrange
    html = '<div id="other">Content</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_id(soup, "main")

    # Assert
    assert result is None


def test_find_elements_by_id_nested_element() -> None:
    """
    Test case 3: Find nested element by ID.
    """
    # Arrange
    html = '<div><section><p id="target">Text</p></section></div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_id(soup, "target")

    # Assert
    assert result is not None
    assert result.text == "Text"


def test_find_elements_by_id_first_match() -> None:
    """
    Test case 4: Return first element when duplicate IDs exist (invalid HTML).
    """
    # Arrange
    html = '<div id="dup">First</div><div id="dup">Second</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = find_elements_by_id(soup, "dup")

    # Assert
    assert result is not None
    assert result.text == "First"


def test_find_elements_by_id_type_error_element() -> None:
    """
    Test case 5: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        find_elements_by_id("not a soup", "main")


def test_find_elements_by_id_type_error_element_id() -> None:
    """
    Test case 6: TypeError for invalid element_id type.
    """
    # Arrange
    html = '<div id="main">Content</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="element_id must be a string"):
        find_elements_by_id(soup, 123)


def test_find_elements_by_id_value_error_empty_id() -> None:
    """
    Test case 7: ValueError for empty element_id.
    """
    # Arrange
    html = '<div id="main">Content</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="element_id cannot be empty"):
        find_elements_by_id(soup, "")


def test_find_elements_by_id_value_error_whitespace_id() -> None:
    """
    Test case 8: ValueError for whitespace-only element_id.
    """
    # Arrange
    html = '<div id="main">Content</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="element_id cannot be empty"):
        find_elements_by_id(soup, "   ")
