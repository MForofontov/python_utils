import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from python_utils.web_scraping_functions.html_parsing.extract_links import extract_links
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    extract_links = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_extract_links_simple_links() -> None:
    """
    Test case 1: Extract simple links.
    """
    # Arrange
    html = '<a href="/page1">Link1</a><a href="/page2">Link2</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_links(soup)

    # Assert
    assert result == ["/page1", "/page2"]


def test_extract_links_absolute_urls() -> None:
    """
    Test case 2: Convert to absolute URLs.
    """
    # Arrange
    html = '<a href="/page1">Link1</a><a href="/page2">Link2</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_links(soup, absolute=True, base_url="https://example.com")

    # Assert
    assert result == ["https://example.com/page1", "https://example.com/page2"]


def test_extract_links_mixed_urls() -> None:
    """
    Test case 3: Extract mixed relative and absolute URLs.
    """
    # Arrange
    html = '<a href="/local">Local</a><a href="https://other.com">External</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_links(soup, absolute=True, base_url="https://example.com")

    # Assert
    assert result == ["https://example.com/local", "https://other.com"]


def test_extract_links_relative_paths() -> None:
    """
    Test case 4: Extract relative paths without leading slash.
    """
    # Arrange
    html = '<a href="page1">Link1</a><a href="page2">Link2</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_links(soup, absolute=True, base_url="https://example.com")

    # Assert
    assert result == ["https://example.com/page1", "https://example.com/page2"]


def test_extract_links_no_links() -> None:
    """
    Test case 5: Extract from HTML with no links.
    """
    # Arrange
    html = "<div>No links here</div>"
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_links(soup)

    # Assert
    assert result == []


def test_extract_links_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        extract_links("not a soup")


def test_extract_links_type_error_absolute() -> None:
    """
    Test case 7: TypeError for invalid absolute type.
    """
    # Arrange
    html = '<a href="/page">Link</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="absolute must be a boolean"):
        extract_links(soup, absolute="yes")


def test_extract_links_type_error_base_url() -> None:
    """
    Test case 8: TypeError for invalid base_url type.
    """
    # Arrange
    html = '<a href="/page">Link</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="base_url must be a string or None"):
        extract_links(soup, base_url=123)


def test_extract_links_value_error_missing_base_url() -> None:
    """
    Test case 9: ValueError when absolute is True but base_url is None.
    """
    # Arrange
    html = '<a href="/page">Link</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(
        ValueError, match="base_url must be provided when absolute is True"
    ):
        extract_links(soup, absolute=True)
