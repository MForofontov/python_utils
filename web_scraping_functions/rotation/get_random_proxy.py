"""
Get random proxy from list.
"""

import random


def get_random_proxy(
    proxies: list[str],
) -> dict[str, str]:
    """
    Get random proxy from list.

    Parameters
    ----------
    proxies : list[str]
        List of proxy URLs.

    Returns
    -------
    dict[str, str]
        Random proxy dictionary for requests.

    Raises
    ------
    TypeError
        If proxies is not a list.
    ValueError
        If proxies list is empty.

    Examples
    --------
    >>> proxies = ["http://proxy1:8080", "http://proxy2:8080"]
    >>> proxy = get_random_proxy(proxies)
    >>> 'http' in proxy
    True

    Notes
    -----
    Uses random.choice for selection.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(proxies, list):
        raise TypeError(f"proxies must be a list, got {type(proxies).__name__}")

    if not proxies:
        raise ValueError("proxies list cannot be empty")

    proxy = random.choice(proxies)
    return {"http": proxy, "https": proxy}


__all__ = ["get_random_proxy"]
