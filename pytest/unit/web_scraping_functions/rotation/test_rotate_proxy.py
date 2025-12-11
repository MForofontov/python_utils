import pytest
from web_scraping_functions.rotation.rotate_proxy import rotate_proxy


def test_rotate_proxy_case_1_basic_rotation() -> None:
    """
    Test case 1: Basic proxy rotation through list.
    """
    # Arrange
    proxies = ["proxy1", "proxy2", "proxy3"]
    rotator = rotate_proxy(proxies)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    result3 = next(rotator)
    result4 = next(rotator)
    
    # Assert
    assert result1 == "proxy1"
    assert result2 == "proxy2"
    assert result3 == "proxy3"
    assert result4 == "proxy1"  # Cycles back


def test_rotate_proxy_case_2_single_proxy() -> None:
    """
    Test case 2: Rotation with single proxy.
    """
    # Arrange
    proxies = ["only_proxy"]
    rotator = rotate_proxy(proxies)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    
    # Assert
    assert result1 == "only_proxy"
    assert result2 == "only_proxy"


def test_rotate_proxy_case_3_infinite_cycling() -> None:
    """
    Test case 3: Verify infinite cycling.
    """
    # Arrange
    proxies = ["proxy1", "proxy2"]
    rotator = rotate_proxy(proxies)
    
    # Act
    results = [next(rotator) for _ in range(10)]
    
    # Assert
    assert results == ["proxy1", "proxy2"] * 5


def test_rotate_proxy_case_4_list_not_modified() -> None:
    """
    Test case 4: Original list is not modified.
    """
    # Arrange
    proxies = ["proxy1", "proxy2", "proxy3"]
    original_proxies = proxies.copy()
    rotator = rotate_proxy(proxies)
    
    # Act
    next(rotator)
    next(rotator)
    
    # Assert
    assert proxies == original_proxies


def test_rotate_proxy_case_5_type_error_proxies() -> None:
    """
    Test case 5: TypeError for invalid proxies type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="proxies must be a list"):
        rotate_proxy("not a list")


def test_rotate_proxy_case_6_value_error_empty_list() -> None:
    """
    Test case 6: ValueError for empty proxy list.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="proxies cannot be empty"):
        rotate_proxy([])


def test_rotate_proxy_case_7_type_error_non_string_elements() -> None:
    """
    Test case 7: TypeError for non-string elements in list.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="all elements in proxies must be strings"):
        rotate_proxy(["proxy1", 123, "proxy3"])


def test_rotate_proxy_case_8_mixed_proxy_formats() -> None:
    """
    Test case 8: Support different proxy string formats.
    """
    # Arrange
    proxies = [
        "http://proxy1.com:8080",
        "https://proxy2.com:3128",
        "socks5://proxy3.com:1080"
    ]
    rotator = rotate_proxy(proxies)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    
    # Assert
    assert result1 == "http://proxy1.com:8080"
    assert result2 == "https://proxy2.com:3128"
