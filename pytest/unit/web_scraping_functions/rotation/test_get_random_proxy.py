import pytest

try:
    from bs4 import BeautifulSoup
    from python_utils.web_scraping_functions.rotation.get_random_proxy import get_random_proxy
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    get_random_proxy = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.web_scraping,
    pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed"),
]


def test_get_random_proxy_returns_from_list() -> None:
    """
    Test case 1: Return a proxy from the list.
    """
    # Arrange
    proxies = ["proxy1", "proxy2", "proxy3"]

    # Act
    result = get_random_proxy(proxies)

    # Assert
    assert isinstance(result, dict)
    assert "http" in result and "https" in result
    assert result["http"] in proxies


def test_get_random_proxy_single_proxy() -> None:
    """
    Test case 2: Return the only proxy from single-element list.
    """
    # Arrange
    proxies = ["only_proxy"]

    # Act
    result = get_random_proxy(proxies)

    # Assert
    assert result == {"http": "only_proxy", "https": "only_proxy"}


def test_get_random_proxy_randomness() -> None:
    """
    Test case 3: Verify random selection over multiple calls.
    """
    # Arrange
    proxies = ["proxy1", "proxy2", "proxy3", "proxy4", "proxy5"]

    # Act
    results = {get_random_proxy(proxies)["http"] for _ in range(50)}

    # Assert - should get at least 2 different proxies in 50 calls
    assert len(results) >= 2


def test_get_random_proxy_list_not_modified() -> None:
    """
    Test case 4: Original list is not modified.
    """
    # Arrange
    proxies = ["proxy1", "proxy2", "proxy3"]
    original_proxies = proxies.copy()

    # Act
    get_random_proxy(proxies)

    # Assert
    assert proxies == original_proxies


def test_get_random_proxy_type_error_proxies() -> None:
    """
    Test case 5: TypeError for invalid proxies type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="proxies must be a list"):
        get_random_proxy("not a list")


def test_get_random_proxy_value_error_empty_list() -> None:
    """
    Test case 6: ValueError for empty proxy list.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="proxies list cannot be empty"):
        get_random_proxy([])


def test_get_random_proxy_proxy_formats() -> None:
    """
    Test case 7: Handle different proxy formats.
    """
    # Arrange
    proxies = [
        "http://proxy1.com:8080",
        "https://proxy2.com:3128",
        "socks5://proxy3.com:1080",
    ]

    # Act
    result = get_random_proxy(proxies)

    # Assert
    assert isinstance(result, dict)
    assert result["http"] in proxies
    assert "://" in result["http"]
