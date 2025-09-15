"""URL building functionality."""

import urllib.parse


def build_url(
    scheme: str,
    hostname: str,
    port: int | None = None,
    path: str = "",
    query_params: dict[str, str] | None = None,
    fragment: str | None = None,
    username: str | None = None,
    password: str | None = None,
) -> str:
    """
    Build a URL from components.

    Parameters
    ----------
    scheme : str
        URL scheme (e.g., 'http', 'https').
    hostname : str
        Hostname or IP address.
    port : int, optional
        Port number.
    path : str, optional
        URL path (default: "").
    query_params : dict of str, optional
        Query parameters as key-value pairs.
    fragment : str, optional
        URL fragment (anchor).
    username : str, optional
        Username for authentication.
    password : str, optional
        Password for authentication.

    Returns
    -------
    str
        The constructed URL.

    Raises
    ------
    ValueError
        If required parameters are invalid.

    Examples
    --------
    >>> build_url('https', 'example.com', path='/api/v1')
    'https://example.com/api/v1'
    >>> build_url('https', 'example.com', query_params={'q': 'search', 'page': '1'})
    'https://example.com?q=search&page=1'
    """
    if not isinstance(scheme, str) or not scheme.strip():
        raise ValueError("Scheme must be a non-empty string")

    if not isinstance(hostname, str) or not hostname.strip():
        raise ValueError("Hostname must be a non-empty string")

    # Build netloc
    netloc = hostname
    if port:
        netloc = f"{hostname}:{port}"

    if username:
        if password:
            netloc = f"{username}:{password}@{netloc}"
        else:
            netloc = f"{username}@{netloc}"

    # Build query string
    query = ""
    if query_params:
        query = urllib.parse.urlencode(query_params)

    # Use urlunparse to build the URL
    url_parts = (scheme, netloc, path, "", query, fragment or "")
    return urllib.parse.urlunparse(url_parts)
