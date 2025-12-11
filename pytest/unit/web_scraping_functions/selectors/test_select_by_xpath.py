import pytest
from bs4 import BeautifulSoup
from web_scraping_functions.selectors.select_by_xpath import select_by_xpath


def test_select_by_xpath_case_1_simple_xpath() -> None:
    """
    Test case 1: Select elements with simple XPath.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = select_by_xpath(soup, '//div[@class="item"]')
    
    # Assert
    assert len(result) == 2


def test_select_by_xpath_case_2_with_limit() -> None:
    """
    Test case 2: Select elements with limit.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div><div class="item">C</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = select_by_xpath(soup, '//div[@class="item"]', limit=2)
    
    # Assert
    assert len(result) == 2


def test_select_by_xpath_case_3_text_selection() -> None:
    """
    Test case 3: Select elements by text content.
    """
    # Arrange
    html = '<p>Hello</p><p>World</p>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = select_by_xpath(soup, '//p[text()="Hello"]')
    
    # Assert
    assert len(result) == 1


def test_select_by_xpath_case_4_nested_selection() -> None:
    """
    Test case 4: Select nested elements.
    """
    # Arrange
    html = '<div><section><p>Text</p></section></div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = select_by_xpath(soup, '//div/section/p')
    
    # Assert
    assert len(result) == 1


def test_select_by_xpath_case_5_no_matches() -> None:
    """
    Test case 5: Return empty list when no matches found.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act
    result = select_by_xpath(soup, '//span[@class="nonexistent"]')
    
    # Assert
    assert result == []


def test_select_by_xpath_case_6_type_error_element() -> None:
    """
    Test case 6: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        select_by_xpath("not a soup", "//div")


def test_select_by_xpath_case_7_type_error_xpath() -> None:
    """
    Test case 7: TypeError for invalid xpath type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(TypeError, match="xpath must be a string"):
        select_by_xpath(soup, 123)


def test_select_by_xpath_case_8_type_error_limit() -> None:
    """
    Test case 8: TypeError for invalid limit type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(TypeError, match="limit must be an integer or None"):
        select_by_xpath(soup, "//div", limit="5")


def test_select_by_xpath_case_9_value_error_empty_xpath() -> None:
    """
    Test case 9: ValueError for empty xpath.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(ValueError, match="xpath cannot be empty"):
        select_by_xpath(soup, "")


def test_select_by_xpath_case_10_value_error_non_positive_limit() -> None:
    """
    Test case 10: ValueError for non-positive limit.
    """
    # Arrange
    html = '<div class="item">A</div>'
    soup = BeautifulSoup(html, "html.parser")
    
    # Act & Assert
    with pytest.raises(ValueError, match="limit must be positive"):
        select_by_xpath(soup, "//div", limit=0)
