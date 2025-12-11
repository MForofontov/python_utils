import pytest
from unittest.mock import Mock
from bs4 import BeautifulSoup
from web_scraping_functions.pagination.paginate_with_callback import (
    paginate_with_callback,
)


def test_paginate_with_callback_case_1_simple_pagination() -> None:
    """
    Test case 1: Paginate with callback collecting results.
    """
    # Arrange
    results = []
    
    def callback(soup: BeautifulSoup, page: int) -> bool:
        results.append(page)
        return page < 3  # Continue until page 3
    
    fetch_func = Mock(return_value="<html><body>Content</body></html>")
    
    # Act
    paginate_with_callback(
        base_url="https://example.com",
        callback=callback,
        start=1,
        fetch_function=fetch_func
    )
    
    # Assert
    assert results == [1, 2, 3]


def test_paginate_with_callback_case_2_max_pages_limit() -> None:
    """
    Test case 2: Respect max_pages limit.
    """
    # Arrange
    pages_visited = []
    
    def callback(soup: BeautifulSoup, page: int) -> bool:
        pages_visited.append(page)
        return True  # Always continue
    
    fetch_func = Mock(return_value="<html><body>Content</body></html>")
    
    # Act
    paginate_with_callback(
        base_url="https://example.com",
        callback=callback,
        start=1,
        max_pages=3,
        fetch_function=fetch_func
    )
    
    # Assert
    assert len(pages_visited) == 3


def test_paginate_with_callback_case_3_callback_stops_pagination() -> None:
    """
    Test case 3: Stop pagination when callback returns False.
    """
    # Arrange
    pages_visited = []
    
    def callback(soup: BeautifulSoup, page: int) -> bool:
        pages_visited.append(page)
        return page < 2  # Stop after page 2
    
    fetch_func = Mock(return_value="<html><body>Content</body></html>")
    
    # Act
    paginate_with_callback(
        base_url="https://example.com",
        callback=callback,
        start=1,
        max_pages=10,
        fetch_function=fetch_func
    )
    
    # Assert
    assert pages_visited == [1, 2]


def test_paginate_with_callback_case_4_custom_page_param() -> None:
    """
    Test case 4: Use custom page parameter.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return page < 2
    
    fetch_func = Mock(return_value="<html><body>Content</body></html>")
    
    # Act
    paginate_with_callback(
        base_url="https://example.com",
        callback=callback,
        start=1,
        page_param="p",
        fetch_function=fetch_func
    )
    
    # Assert
    calls = fetch_func.call_args_list
    assert "p=1" in calls[0][0][0]


def test_paginate_with_callback_case_5_type_error_base_url() -> None:
    """
    Test case 5: TypeError for invalid base_url type.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return False
    
    # Act & Assert
    with pytest.raises(TypeError, match="base_url must be a string"):
        paginate_with_callback(123, callback=callback)


def test_paginate_with_callback_case_6_type_error_callback() -> None:
    """
    Test case 6: TypeError for invalid callback type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="callback must be callable"):
        paginate_with_callback("https://example.com", callback="not callable")


def test_paginate_with_callback_case_7_type_error_start() -> None:
    """
    Test case 7: TypeError for invalid start type.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return False
    
    # Act & Assert
    with pytest.raises(TypeError, match="start must be an integer"):
        paginate_with_callback("https://example.com", callback=callback, start="1")


def test_paginate_with_callback_case_8_type_error_max_pages() -> None:
    """
    Test case 8: TypeError for invalid max_pages type.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return False
    
    # Act & Assert
    with pytest.raises(TypeError, match="max_pages must be an integer or None"):
        paginate_with_callback(
            "https://example.com",
            callback=callback,
            max_pages="10"
        )


def test_paginate_with_callback_case_9_value_error_negative_start() -> None:
    """
    Test case 9: ValueError for negative start.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return False
    
    # Act & Assert
    with pytest.raises(ValueError, match="start must be non-negative"):
        paginate_with_callback("https://example.com", callback=callback, start=-1)


def test_paginate_with_callback_case_10_value_error_non_positive_max_pages() -> None:
    """
    Test case 10: ValueError for non-positive max_pages.
    """
    # Arrange
    def callback(soup: BeautifulSoup, page: int) -> bool:
        return False
    
    # Act & Assert
    with pytest.raises(ValueError, match="max_pages must be positive"):
        paginate_with_callback(
            "https://example.com",
            callback=callback,
            max_pages=0
        )
