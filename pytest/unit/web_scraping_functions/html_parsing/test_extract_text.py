import pytest
from bs4 import BeautifulSoup
from web_scraping_functions.html_parsing.extract_text import extract_text


def test_extract_text_simple_text() -> None:
    """
    Test case 1: Extract text from simple element.
    """
    # Arrange
    html = "<div>Hello World</div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = extract_text(soup)
    
    # Assert
    assert result == "Hello World"


def test_extract_text_nested_elements() -> None:
    """
    Test case 2: Extract text from nested elements.
    """
    # Arrange
    html = "<div>Hello <span>Beautiful</span> World</div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = extract_text(soup)
    
    # Assert
    assert result == "Hello Beautiful World"


def test_extract_text_with_whitespace() -> None:
    """
    Test case 3: Extract text with whitespace handling.
    """
    # Arrange
    html = "<div>  Hello  <span>  World  </span>  </div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = extract_text(soup, strip=True)
    
    # Assert
    assert result == "Hello World"


def test_extract_text_no_strip() -> None:
    """
    Test case 4: Extract text without stripping.
    """
    # Arrange
    html = "<div>  Hello  </div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = extract_text(soup, strip=False)
    
    # Assert
    assert "  Hello  " in result


def test_extract_text_custom_separator() -> None:
    """
    Test case 5: Extract text with custom separator.
    """
    # Arrange
    html = "<div>Hello<br/>World</div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = extract_text(soup, separator="-")
    
    # Assert
    assert "Hello" in result and "World" in result


def test_extract_text_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        extract_text("not a soup object")


def test_extract_text_type_error_strip() -> None:
    """
    Test case 7: TypeError for invalid strip type.
    """
    # Arrange
    html = "<div>Test</div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(TypeError, match="strip must be a boolean"):
        extract_text(soup, strip="yes")


def test_extract_text_type_error_separator() -> None:
    """
    Test case 8: TypeError for invalid separator type.
    """
    # Arrange
    html = "<div>Test</div>"
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(TypeError, match="separator must be a string"):
        extract_text(soup, separator=123)
