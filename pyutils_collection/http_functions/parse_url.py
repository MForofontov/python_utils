"""URL parsing functionality."""

import urllib.parse
from typing import Any


def parse_url(url: str) -> dict[str, Any]:
    """
    Parse a URL into its components.

    Parameters
    ----------
    url : str
        The URL to parse.

    Returns
    -------
    dict
        Dictionary containing URL components: 'scheme', 'netloc', 'hostname',
        'port', 'path', 'params', 'query', 'fragment', 'username', 'password'.

    Raises
    ------
    TypeError
        If the provided URL is not a string.
    ValueError
        If the URL string is empty or only whitespace.

    Examples
    --------
    >>> result = parse_url('https://user:pass@example.com:8080/path?query=value#fragment')
    >>> result['scheme']
    'https'
    >>> result['hostname']
    'example.com'
    >>> result['port']
    8080
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")

    if not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urllib.parse.urlparse(url)

    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "username": parsed.username,
        "password": parsed.password,
    }
