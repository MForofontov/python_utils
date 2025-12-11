import pytest
from web_scraping_functions.pagination.paginate_links import paginate_links


def test_paginate_links_case_1_simple_pagination() -> None:
    """
    Test case 1: Generate simple pagination URLs.
    """
    # Arrange
    base_url = "https://example.com/page"
    
    # Act
    result = list(paginate_links(base_url, start=1, end=3))
    
    # Assert
    assert result == [
        "https://example.com/page?page=1",
        "https://example.com/page?page=2",
        "https://example.com/page?page=3"
    ]


def test_paginate_links_case_2_custom_param() -> None:
    """
    Test case 2: Generate pagination with custom parameter name.
    """
    # Arrange
    base_url = "https://example.com/items"
    
    # Act
    result = list(paginate_links(base_url, start=1, end=2, page_param="p"))
    
    # Assert
    assert result == [
        "https://example.com/items?p=1",
        "https://example.com/items?p=2"
    ]


def test_paginate_links_case_3_existing_query_params() -> None:
    """
    Test case 3: Add pagination to URL with existing query parameters.
    """
    # Arrange
    base_url = "https://example.com/search?q=test"
    
    # Act
    result = list(paginate_links(base_url, start=1, end=2))
    
    # Assert
    assert result == [
        "https://example.com/search?q=test&page=1",
        "https://example.com/search?q=test&page=2"
    ]


def test_paginate_links_case_4_single_page() -> None:
    """
    Test case 4: Generate single page URL.
    """
    # Arrange
    base_url = "https://example.com/page"
    
    # Act
    result = list(paginate_links(base_url, start=5, end=5))
    
    # Assert
    assert result == ["https://example.com/page?page=5"]


def test_paginate_links_case_5_zero_start() -> None:
    """
    Test case 5: Generate pagination starting from 0.
    """
    # Arrange
    base_url = "https://example.com/items"
    
    # Act
    result = list(paginate_links(base_url, start=0, end=2))
    
    # Assert
    assert len(result) == 3
    assert "page=0" in result[0]


def test_paginate_links_case_6_type_error_base_url() -> None:
    """
    Test case 6: TypeError for invalid base_url type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="base_url must be a string"):
        list(paginate_links(123, start=1, end=3))


def test_paginate_links_case_7_type_error_start() -> None:
    """
    Test case 7: TypeError for invalid start type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="start must be an integer"):
        list(paginate_links("https://example.com", start="1", end=3))


def test_paginate_links_case_8_type_error_end() -> None:
    """
    Test case 8: TypeError for invalid end type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="end must be an integer"):
        list(paginate_links("https://example.com", start=1, end="3"))


def test_paginate_links_case_9_type_error_page_param() -> None:
    """
    Test case 9: TypeError for invalid page_param type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="page_param must be a string"):
        list(paginate_links("https://example.com", start=1, end=3, page_param=123))


def test_paginate_links_case_10_value_error_empty_url() -> None:
    """
    Test case 10: ValueError for empty base_url.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="base_url cannot be empty"):
        list(paginate_links("", start=1, end=3))


def test_paginate_links_case_11_value_error_negative_start() -> None:
    """
    Test case 11: ValueError for negative start.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="start must be non-negative"):
        list(paginate_links("https://example.com", start=-1, end=3))


def test_paginate_links_case_12_value_error_invalid_range() -> None:
    """
    Test case 12: ValueError when start > end.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="start must be less than or equal to end"):
        list(paginate_links("https://example.com", start=5, end=3))
