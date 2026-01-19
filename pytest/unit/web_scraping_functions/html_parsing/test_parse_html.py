import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from python_utils.web_scraping_functions.html_parsing.parse_html import parse_html
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    parse_html = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_parse_html_simple_html() -> None:
    """
    Test case 1: Parse simple HTML content.
    """
    # Arrange
    html = "<html><body><p>Hello World</p></body></html>"

    # Act
    result = parse_html(html)

    # Assert
    assert isinstance(result, BeautifulSoup)
    assert result.find("p").text == "Hello World"


def test_parse_html_with_lxml_parser() -> None:
    """
    Test case 2: Parse HTML with lxml parser.
    """
    # Arrange
    html = "<html><body><div>Content</div></body></html>"

    # Act
    result = parse_html(html, parser="lxml")

    # Assert
    assert isinstance(result, BeautifulSoup)
    assert result.find("div").text == "Content"


def test_parse_html_complex_structure() -> None:
    """
    Test case 3: Parse HTML with complex structure.
    """
    # Arrange
    html = "<html><head><title>Test</title></head><body><div class='main'><p>Text</p></div></body></html>"

    # Act
    result = parse_html(html)

    # Assert
    assert result.title.text == "Test"
    assert result.find("div", class_="main") is not None


def test_parse_html_default_parser() -> None:
    """
    Test case 4: Verify default parser is html.parser.
    """
    # Arrange
    html = "<html><body>Test</body></html>"

    # Act
    result = parse_html(html)

    # Assert
    assert result.name == "[document]"


def test_parse_html_type_error_html() -> None:
    """
    Test case 5: TypeError for invalid html type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="html must be a string"):
        parse_html(123)


def test_parse_html_type_error_parser() -> None:
    """
    Test case 6: TypeError for invalid parser type.
    """
    # Arrange
    html = "<html><body>Test</body></html>"

    # Act & Assert
    with pytest.raises(TypeError, match="parser must be a string"):
        parse_html(html, parser=123)


def test_parse_html_value_error_empty_html() -> None:
    """
    Test case 7: ValueError for empty HTML.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="html cannot be empty"):
        parse_html("")


def test_parse_html_value_error_whitespace_only() -> None:
    """
    Test case 8: ValueError for whitespace-only HTML.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="html cannot be empty"):
        parse_html("   \n  \t  ")


def test_parse_html_value_error_invalid_parser() -> None:
    """
    Test case 9: ValueError for invalid parser name.
    """
    # Arrange
    html = "<html><body>Test</body></html>"

    # Act & Assert
    with pytest.raises(ValueError, match="parser must be one of"):
        parse_html(html, parser="invalid_parser")
