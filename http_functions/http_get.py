"""Simple HTTP GET request functionality."""

import urllib.request
from typing import Any
from urllib.error import HTTPError, URLError


def http_get(
    url: str, headers: dict[str, str] | None = None, timeout: int = 30
) -> dict[str, Any]:
    """
    Perform a simple HTTP GET request.

    Parameters
    ----------
    url : str
        The URL to send the GET request to.
    headers : dict of str, optional
        HTTP headers to include in the request.
    timeout : int, optional
        Timeout in seconds (default: 30).

    Returns
    -------
    dict
        Dictionary containing 'status_code', 'content', 'headers', and 'url'.

    Raises
    ------
    TypeError
        If ``url`` is not provided as a string.
    ValueError
        If ``url`` is an empty or whitespace-only string.

    Examples
    --------
    >>> response = http_get('https://httpbin.org/get')
    >>> response['status_code']
    200
    >>> 'content' in response
    True
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")

    if not url.strip():
        raise ValueError("URL must be a non-empty string")

    # Create request
    req = urllib.request.Request(url)

    # Add headers if provided
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8")
            return {
                "status_code": response.getcode(),
                "content": content,
                "headers": dict(response.headers),
                "url": response.geturl(),
            }
    except HTTPError as e:
        return {
            "status_code": e.code,
            "content": e.read().decode("utf-8") if e.fp else "",
            "headers": dict(e.headers) if e.headers else {},
            "url": url,
        }
    except URLError as e:
        return {
            "status_code": None,
            "content": str(e.reason),
            "headers": {},
            "url": url,
        }
