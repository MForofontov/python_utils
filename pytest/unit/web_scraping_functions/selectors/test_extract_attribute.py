import pytest
from bs4 import BeautifulSoup
from web_scraping_functions.selectors.extract_attribute import extract_attribute


def test_extract_attribute_simple_attribute() -> None:
    """
    Test case 1: Extract simple attribute from element.
    """
    # Arrange
    html = '<a href="/page">Link</a>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('a')
    
    # Act
    result = extract_attribute(element, "href")
    
    # Assert
    assert result == "/page"


def test_extract_attribute_class_attribute() -> None:
    """
    Test case 2: Extract class attribute.
    """
    # Arrange
    html = '<div class="main content">Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act
    result = extract_attribute(element, "class")
    
    # Assert
    assert result == ["main", "content"]


def test_extract_attribute_missing_attribute() -> None:
    """
    Test case 3: Return None when attribute doesn't exist.
    """
    # Arrange
    html = '<div>Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act
    result = extract_attribute(element, "href")
    
    # Assert
    assert result is None


def test_extract_attribute_default_value() -> None:
    """
    Test case 4: Return default value when attribute missing.
    """
    # Arrange
    html = '<div>Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act
    result = extract_attribute(element, "href", default="default_value")
    
    # Assert
    assert result == "default_value"


def test_extract_attribute_id_attribute() -> None:
    """
    Test case 5: Extract id attribute.
    """
    # Arrange
    html = '<div id="main">Content</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act
    result = extract_attribute(element, "id")
    
    # Assert
    assert result == "main"


def test_extract_attribute_data_attribute() -> None:
    """
    Test case 6: Extract data-* attribute.
    """
    # Arrange
    html = '<div data-value="123">Content</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act
    result = extract_attribute(element, "data-value")
    
    # Assert
    assert result == "123"


def test_extract_attribute_type_error_element() -> None:
    """
    Test case 7: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be a Tag"):
        extract_attribute("not a tag", "href")


def test_extract_attribute_type_error_attribute() -> None:
    """
    Test case 8: TypeError for invalid attribute type.
    """
    # Arrange
    html = '<div>Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act & Assert
    with pytest.raises(TypeError, match="attribute must be a string"):
        extract_attribute(element, 123)  # type: ignore


def test_extract_attribute_value_error_empty_attribute() -> None:
    """
    Test case 9: ValueError for empty attribute.
    """
    # Arrange
    html = '<div>Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act & Assert
    with pytest.raises(ValueError, match="attribute cannot be empty"):
        extract_attribute(element, "")


def test_extract_attribute_whitespace_attribute() -> None:
    """
    Test case 10: ValueError for whitespace-only attribute.
    """
    # Arrange
    html = '<div>Text</div>'
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find('div')
    
    # Act & Assert
    with pytest.raises(ValueError, match="attribute cannot be empty"):
        extract_attribute(element, "   ")
