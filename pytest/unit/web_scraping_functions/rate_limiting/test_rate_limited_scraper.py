import pytest
import time
from unittest.mock import Mock
from web_scraping_functions.rate_limiting.rate_limited_scraper import (
    rate_limited_scraper,
)


def test_rate_limited_scraper_basic_rate_limiting() -> None:
    """
    Test case 1: Apply basic rate limiting to function.
    """
    # Arrange
    @rate_limited_scraper(calls_per_second=10)
    def scrape_page(url: str) -> str:
        return f"Content from {url}"
    
    # Act
    start_time = time.time()
    result1 = scrape_page("https://example.com/1")
    result2 = scrape_page("https://example.com/2")
    elapsed = time.time() - start_time
    
    # Assert
    assert result1 == "Content from https://example.com/1"
    assert result2 == "Content from https://example.com/2"
    assert elapsed >= 0.1  # At least 0.1 seconds between calls (1/10)


def test_rate_limited_scraper_preserves_function_signature() -> None:
    """
    Test case 2: Decorator preserves function metadata.
    """
    # Arrange
    @rate_limited_scraper(calls_per_second=5)
    def my_scraper(url: str) -> str:
        """Scrape a URL."""
        return url
    
    # Act & Assert
    assert my_scraper.__name__ == "my_scraper"
    assert "Scrape a URL" in my_scraper.__doc__


def test_rate_limited_scraper_different_rates() -> None:
    """
    Test case 3: Apply different rate limits.
    """
    # Arrange
    @rate_limited_scraper(calls_per_second=2)
    def slow_scraper(url: str) -> str:
        return url
    
    # Act
    start_time = time.time()
    slow_scraper("url1")
    slow_scraper("url2")
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 0.5  # At least 0.5 seconds between calls (1/2)


def test_rate_limited_scraper_with_kwargs() -> None:
    """
    Test case 4: Function with keyword arguments.
    """
    # Arrange
    @rate_limited_scraper(calls_per_second=10)
    def scraper_with_options(url: str, timeout: int = 30) -> str:
        return f"{url}-{timeout}"
    
    # Act
    result = scraper_with_options("https://example.com", timeout=60)
    
    # Assert
    assert result == "https://example.com-60"


def test_rate_limited_scraper_type_error_calls_per_second() -> None:
    """
    Test case 5: TypeError for invalid calls_per_second type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="calls_per_second must be a number"):
        @rate_limited_scraper(calls_per_second="5")
        def scraper(url: str) -> str:
            return url


def test_rate_limited_scraper_value_error_non_positive_rate() -> None:
    """
    Test case 6: ValueError for non-positive calls_per_second.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="calls_per_second must be positive"):
        @rate_limited_scraper(calls_per_second=0)
        def scraper(url: str) -> str:
            return url


def test_rate_limited_scraper_value_error_negative_rate() -> None:
    """
    Test case 7: ValueError for negative calls_per_second.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="calls_per_second must be positive"):
        @rate_limited_scraper(calls_per_second=-1)
        def scraper(url: str) -> str:
            return url


def test_rate_limited_scraper_exception_propagation() -> None:
    """
    Test case 8: Exceptions from wrapped function are propagated.
    """
    # Arrange
    @rate_limited_scraper(calls_per_second=10)
    def failing_scraper(url: str) -> str:
        raise ValueError("Scraping failed")
    
    # Act & Assert
    with pytest.raises(ValueError, match="Scraping failed"):
        failing_scraper("https://example.com")
