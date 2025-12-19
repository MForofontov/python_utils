import pytest
from web_scraping_functions.pagination.paginate_with_callback import (
    paginate_with_callback,
)


def test_paginate_with_callback_simple_pagination() -> None:
    """
    Test case 1: Paginate with callback collecting results.
    """
    # Arrange
    collected_data = []
    
    def callback(url: str) -> tuple[dict, str | None]:
        page_num = int(url.split("=")[-1]) if "page=" in url else 1
        data = {"page": page_num}
        collected_data.append(data)
        next_url = f"https://example.com?page={page_num + 1}" if page_num < 3 else None
        return data, next_url
    
    # Act
    results = paginate_with_callback(
        start_url="https://example.com?page=1",
        callback=callback,
        max_pages=5
    )
    
    # Assert
    assert len(results) == 3
    assert len(collected_data) == 3


def test_paginate_with_callback_max_pages_limit() -> None:
    """
    Test case 2: Respect max_pages limit.
    """
    # Arrange
    def callback(url: str) -> tuple[dict, str | None]:
        page_num = int(url.split("=")[-1]) if "page=" in url else 1
        data = {"page": page_num}
        next_url = f"https://example.com?page={page_num + 1}"
        return data, next_url
    
    # Act
    results = paginate_with_callback(
        start_url="https://example.com?page=1",
        callback=callback,
        max_pages=3
    )
    
    # Assert
    assert len(results) == 3


def test_paginate_with_callback_callback_stops_pagination() -> None:
    """
    Test case 3: Stop pagination when callback returns None.
    """
    # Arrange
    def callback(url: str) -> tuple[dict, str | None]:
        page_num = int(url.split("=")[-1]) if "page=" in url else 1
        data = {"page": page_num}
        next_url = f"https://example.com?page={page_num + 1}" if page_num < 2 else None
        return data, next_url
    
    # Act
    results = paginate_with_callback(
        start_url="https://example.com?page=1",
        callback=callback,
        max_pages=10
    )
    
    # Assert
    assert len(results) == 2


def test_paginate_with_callback_collect_different_data() -> None:
    """
    Test case 4: Collect different data types.
    """
    # Arrange
    def callback(url: str) -> tuple[list, str | None]:
        page_num = int(url.split("=")[-1]) if "page=" in url else 1
        data = [f"item{page_num}"]
        next_url = f"https://example.com?page={page_num + 1}" if page_num < 2 else None
        return data, next_url
    
    # Act
    results = paginate_with_callback(
        start_url="https://example.com?page=1",
        callback=callback,
        max_pages=5
    )
    
    # Assert
    assert len(results) == 2
    assert results[0] == ["item1"]


def test_paginate_with_callback_type_error_start_url() -> None:
    """
    Test case 5: TypeError for invalid start_url type.
    """
    # Arrange
    def callback(url: str) -> tuple[dict[str, int], str | None]:
        return {"page": 1}, None
    
    # Act & Assert
    with pytest.raises(TypeError, match="start_url must be a string"):
        paginate_with_callback(123, callback=callback)  # type: ignore


def test_paginate_with_callback_type_error_callback() -> None:
    """
    Test case 6: TypeError for invalid callback type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="callback must be callable"):
        paginate_with_callback("https://example.com", callback="not callable")  # type: ignore


def test_paginate_with_callback_type_error_max_pages() -> None:
    """
    Test case 7: TypeError for invalid max_pages type.
    """
    # Arrange
    def callback(url: str) -> tuple[dict[str, int], str | None]:
        return {"page": 1}, None
    
    # Act & Assert
    with pytest.raises(TypeError, match="max_pages must be an integer"):
        paginate_with_callback(
            "https://example.com",
            callback=callback,
            max_pages="10"  # type: ignore
        )


def test_paginate_with_callback_value_error_empty_start_url() -> None:
    """
    Test case 8: ValueError for empty start_url.
    """
    # Arrange
    def callback(url: str) -> tuple[dict[str, int], str | None]:
        return {"page": 1}, None
    
    # Act & Assert
    with pytest.raises(ValueError, match="start_url cannot be empty"):
        paginate_with_callback("", callback=callback)


def test_paginate_with_callback_value_error_non_positive_max_pages() -> None:
    """
    Test case 9: ValueError for non-positive max_pages.
    """
    # Arrange
    def callback(url: str) -> tuple[dict[str, int], str | None]:
        return {"page": 1}, None
    
    # Act & Assert
    with pytest.raises(ValueError, match="max_pages must be positive"):
        paginate_with_callback(
            "https://example.com",
            callback=callback,
            max_pages=0
        )
