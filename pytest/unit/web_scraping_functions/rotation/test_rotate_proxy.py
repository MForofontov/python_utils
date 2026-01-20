import pytest

try:
    from bs4 import BeautifulSoup
    from pyutils_collection.web_scraping_functions.rotation.rotate_proxy import rotate_proxy
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    rotate_proxy = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.web_scraping,
    pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed"),
]


def test_rotate_proxy_basic_rotation() -> None:
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
    assert result1 == {"http": "proxy1", "https": "proxy1"}
    assert result2 == {"http": "proxy2", "https": "proxy2"}
    assert result3 == {"http": "proxy3", "https": "proxy3"}
    assert result4 == {"http": "proxy1", "https": "proxy1"}  # Cycles back


def test_rotate_proxy_single_proxy() -> None:
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
    assert result1 == {"http": "only_proxy", "https": "only_proxy"}
    assert result2 == {"http": "only_proxy", "https": "only_proxy"}


def test_rotate_proxy_infinite_cycling() -> None:
    """
    Test case 3: Verify infinite cycling.
    """
    # Arrange
    proxies = ["proxy1", "proxy2"]
    rotator = rotate_proxy(proxies)

    # Act
    results = [next(rotator) for _ in range(10)]

    # Assert
    expected = [
        {"http": "proxy1", "https": "proxy1"},
        {"http": "proxy2", "https": "proxy2"},
    ] * 5
    assert results == expected


def test_rotate_proxy_list_not_modified() -> None:
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


def test_rotate_proxy_type_error_proxies() -> None:
    """
    Test case 5: TypeError for invalid proxies type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="proxies must be a list"):
        rotator = rotate_proxy("not a list")  # type: ignore
        next(rotator)


def test_rotate_proxy_value_error_empty_list() -> None:
    """
    Test case 6: ValueError for empty proxy list.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="proxies list cannot be empty"):
        rotator = rotate_proxy([])
        next(rotator)


def test_rotate_proxy_mixed_proxy_formats() -> None:
    """
    Test case 7: Support different proxy string formats.
    """
    # Arrange
    proxies = [
        "http://proxy1.com:8080",
        "https://proxy2.com:3128",
        "socks5://proxy3.com:1080",
    ]
    rotator = rotate_proxy(proxies)

    # Act
    result1 = next(rotator)
    result2 = next(rotator)

    # Assert
    assert result1 == {
        "http": "http://proxy1.com:8080",
        "https": "http://proxy1.com:8080",
    }
    assert result2 == {
        "http": "https://proxy2.com:3128",
        "https": "https://proxy2.com:3128",
    }
