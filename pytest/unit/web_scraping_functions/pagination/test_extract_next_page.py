import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from web_scraping_functions.pagination.extract_next_page import extract_next_page
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    extract_next_page = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_extract_next_page_simple_next_link() -> None:
    """
    Test case 1: Extract next page link.
    """
    # Arrange
    html = '<a href="/page2" class="next">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_next_page(soup, selector=".next")

    # Assert
    assert result == "/page2"


def test_extract_next_page_relative_url() -> None:
    """
    Test case 2: Extract relative URL.
    """
    # Arrange
    html = '<a href="/page2" class="next">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_next_page(soup, selector=".next")

    # Assert
    assert result == "/page2"


def test_extract_next_page_no_match() -> None:
    """
    Test case 3: Return None when no match found.
    """
    # Arrange
    html = '<a href="/page2" class="prev">Previous</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_next_page(soup, selector=".next")

    # Assert
    assert result is None


def test_extract_next_page_no_href() -> None:
    """
    Test case 4: Return None when element has no href.
    """
    # Arrange
    html = '<a class="next">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_next_page(soup, selector=".next")

    # Assert
    assert result is None


def test_extract_next_page_attribute_selector() -> None:
    """
    Test case 5: Extract using attribute selector.
    """
    # Arrange
    html = '<a href="/page2" rel="next">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_next_page(soup, selector='a[rel="next"]')

    # Assert
    assert result == "/page2"


def test_extract_next_page_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        extract_next_page("not a soup", selector=".next")


def test_extract_next_page_type_error_selector() -> None:
    """
    Test case 7: TypeError for invalid selector type.
    """
    # Arrange
    html = '<a href="/page2">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="selector must be a string"):
        extract_next_page(soup, selector=123)


def test_extract_next_page_value_error_empty_selector() -> None:
    """
    Test case 8: ValueError for empty selector.
    """
    # Arrange
    html = '<a href="/page2">Next</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="selector cannot be empty"):
        extract_next_page(soup, selector="")
