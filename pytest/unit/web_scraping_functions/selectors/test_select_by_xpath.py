import pytest
from lxml import etree
from web_scraping_functions.selectors.select_by_xpath import select_by_xpath


def test_select_by_xpath_case_1_simple_xpath() -> None:
    """
    Test case 1: Select elements with simple XPath.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div>'
    
    # Act
    result = select_by_xpath(html, '//div[@class="item"]')
    
    # Assert
    assert len(result) == 2
    assert all(isinstance(elem, etree._Element) for elem in result)


def test_select_by_xpath_case_2_single_element() -> None:
    """
    Test case 2: Select single element.
    """
    # Arrange
    html = '<div class="item">A</div><div class="item">B</div><div class="item">C</div>'
    
    # Act
    result = select_by_xpath(html, '//div[@class="item"][1]')
    
    # Assert
    assert len(result) == 1


def test_select_by_xpath_case_3_text_selection() -> None:
    """
    Test case 3: Select elements by text content.
    """
    # Arrange
    html = '<p>Hello</p><p>World</p>'
    
    # Act
    result = select_by_xpath(html, '//p[text()="Hello"]')
    
    # Assert
    assert len(result) == 1


def test_select_by_xpath_case_4_nested_selection() -> None:
    """
    Test case 4: Select nested elements.
    """
    # Arrange
    html = '<div><section><p>Text</p></section></div>'
    
    # Act
    result = select_by_xpath(html, '//div/section/p')
    
    # Assert
    assert len(result) == 1


def test_select_by_xpath_case_5_no_matches() -> None:
    """
    Test case 5: Return empty list when no matches found.
    """
    # Arrange
    html = '<div class="item">A</div>'
    
    # Act
    result = select_by_xpath(html, '//span[@class="nonexistent"]')
    
    # Assert
    assert result == []


def test_select_by_xpath_case_6_type_error_html() -> None:
    """
    Test case 6: TypeError for invalid html type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="html must be a string"):
        select_by_xpath(123, "//div")  # type: ignore


def test_select_by_xpath_case_7_type_error_xpath() -> None:
    """
    Test case 7: TypeError for invalid xpath type.
    """
    # Arrange
    html = '<div class="item">A</div>'
    
    # Act & Assert
    with pytest.raises(TypeError, match="xpath must be a string"):
        select_by_xpath(html, 123)  # type: ignore


def test_select_by_xpath_case_8_value_error_empty_html() -> None:
    """
    Test case 8: ValueError for empty html.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="html cannot be empty"):
        select_by_xpath("", "//div")


def test_select_by_xpath_case_9_value_error_empty_xpath() -> None:
    """
    Test case 9: ValueError for empty xpath.
    """
    # Arrange
    html = '<div class="item">A</div>'
    
    # Act & Assert
    with pytest.raises(ValueError, match="xpath cannot be empty"):
        select_by_xpath(html, "")
