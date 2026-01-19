import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from web_scraping_functions.selectors.select_by_css import select_by_css
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    select_by_css = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_select_by_css_simple_selector() -> None:
    """
    Test case 1: Select elements with simple CSS selector.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = select_by_css(soup, ".item")

    # Assert
    assert len(result) == 2
    assert result[0].text == "A"
    assert result[1].text == "B"


def test_select_by_css_with_limit() -> None:
    """
    Test case 2: Select elements with limit.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div><div class="item">C</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = select_by_css(soup, ".item", limit=2)

    # Assert
    assert len(result) == 2


def test_select_by_css_complex_selector() -> None:
    """
    Test case 3: Use complex CSS selector.
    """
    # Arrange
    html = '<div class="outer"><p class="inner">Text</p></div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = select_by_css(soup, "div.outer p.inner")

    # Assert
    assert len(result) == 1
    assert result[0].text == "Text"


def test_select_by_css_attribute_selector() -> None:
    """
    Test case 4: Use attribute selector.
    """
    # Arrange
    html = '<a href="/page1">Link1</a><a href="/page2">Link2</a>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = select_by_css(soup, 'a[href="/page1"]')

    # Assert
    assert len(result) == 1
    assert result[0].text == "Link1"


def test_select_by_css_no_matches() -> None:
    """
    Test case 5: Return empty list when no matches found.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = select_by_css(soup, ".nonexistent")

    # Assert
    assert result == []


def test_select_by_css_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        select_by_css("not a soup", ".item")


def test_select_by_css_type_error_selector() -> None:
    """
    Test case 7: TypeError for invalid selector type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="selector must be a string"):
        select_by_css(soup, 123)


def test_select_by_css_type_error_limit() -> None:
    """
    Test case 8: TypeError for invalid limit type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="limit must be an integer or None"):
        select_by_css(soup, ".item", limit="5")


def test_select_by_css_value_error_empty_selector() -> None:
    """
    Test case 9: ValueError for empty selector.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="selector cannot be empty"):
        select_by_css(soup, "")


def test_select_by_css_value_error_non_positive_limit() -> None:
    """
    Test case 10: ValueError for non-positive limit.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(ValueError, match="limit must be positive"):
        select_by_css(soup, ".item", limit=0)
