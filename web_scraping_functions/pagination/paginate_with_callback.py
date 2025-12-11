"""
Paginate with callback function.
"""

from collections.abc import Callable
from typing import Any


def paginate_with_callback(
    start_url: str,
    callback: Callable[[str], tuple[Any, str | None]],
    max_pages: int = 100,
) -> list[Any]:
    """
    Paginate through pages using callback function.

    Parameters
    ----------
    start_url : str
        Starting URL.
    callback : Callable[[str], tuple[Any, str | None]]
        Function that takes URL and returns (data, next_url).
    max_pages : int, optional
        Maximum pages to fetch (by default 100).

    Returns
    -------
    list[Any]
        List of data from all pages.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If start_url is empty or max_pages is non-positive.

    Examples
    --------
    >>> def fetch_page(url):
    ...     # Simulate fetching page
    ...     data = {"url": url, "items": [1, 2, 3]}
    ...     next_url = None if url.endswith("2") else url + "2"
    ...     return data, next_url
    >>> results = paginate_with_callback("https://example.com/page1", fetch_page, 5)
    >>> len(results)
    2

    Notes
    -----
    Stops when callback returns None as next_url or max_pages is reached.

    Complexity
    ----------
    Time: O(n), Space: O(n), where n is number of pages
    """
    if not isinstance(start_url, str):
        raise TypeError(f"start_url must be a string, got {type(start_url).__name__}")
    if not callable(callback):
        raise TypeError(f"callback must be callable, got {type(callback).__name__}")
    if not isinstance(max_pages, int):
        raise TypeError(f"max_pages must be an integer, got {type(max_pages).__name__}")
    
    if not start_url.strip():
        raise ValueError("start_url cannot be empty")
    
    if max_pages <= 0:
        raise ValueError(f"max_pages must be positive, got {max_pages}")
    
    results = []
    current_url: str | None = start_url
    pages_fetched = 0
    
    while current_url and pages_fetched < max_pages:
        data, next_url = callback(current_url)
        results.append(data)
        current_url = next_url
        pages_fetched += 1
    
    return results


__all__ = ['paginate_with_callback']
