"""
Rotate proxies for requests.
"""

from collections.abc import Iterator


def rotate_proxy(
    proxies: list[str],
) -> Iterator[dict[str, str]]:
    """
    Create proxy rotator that cycles through proxy list.

    Parameters
    ----------
    proxies : list[str]
        List of proxy URLs.

    Yields
    ------
    dict[str, str]
        Proxy dictionary for requests.

    Raises
    ------
    TypeError
        If proxies is not a list.
    ValueError
        If proxies list is empty.

    Examples
    --------
    >>> proxies = ["http://proxy1:8080", "http://proxy2:8080"]
    >>> rotator = rotate_proxy(proxies)
    >>> next(rotator)
    {'http': 'http://proxy1:8080', 'https': 'http://proxy1:8080'}
    >>> next(rotator)
    {'http': 'http://proxy2:8080', 'https': 'http://proxy2:8080'}

    Notes
    -----
    Infinitely cycles through proxy list.

    Complexity
    ----------
    Time: O(1) per iteration, Space: O(1)
    """
    if not isinstance(proxies, list):
        raise TypeError(f"proxies must be a list, got {type(proxies).__name__}")

    if not proxies:
        raise ValueError("proxies list cannot be empty")

    index = 0
    while True:
        proxy = proxies[index % len(proxies)]
        yield {"http": proxy, "https": proxy}
        index += 1


__all__ = ["rotate_proxy"]
