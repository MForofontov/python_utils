"""URL validation functionality."""

from urllib.parse import urlparse

def is_valid_url(url: str, allowed_schemes: list[str] | None = None) -> bool:
    """
    Validate if a string is a valid URL.

    Parameters
    ----------
    url : str
        The URL to validate.
    allowed_schemes : list of str, optional
        List of allowed schemes (e.g., ['http', 'https']).

    Returns
    -------
    bool
        True if the URL is valid, False otherwise.

    Examples
    --------
    >>> is_valid_url('https://example.com')
    True
    >>> is_valid_url('ftp://example.com', ['http', 'https'])
    False
    """
    try:
        # URL must not contain spaces
        if " " in url:
            return False
        result = urlparse(url)
        if allowed_schemes is not None:
            if not allowed_schemes:
                return False
            if result.scheme not in allowed_schemes:
                return False
        if not result.scheme:
            return False
        # For file scheme, allow empty netloc if path is present
        if result.scheme == "file":
            return bool(result.path and result.path.strip())
        if not result.netloc:
            return False
        # Basic hostname validation
        hostname = result.hostname
        if hostname is None:
            return False
        # Hostname must not be empty, must not contain spaces, and must not start with a dot
        if hostname.strip() == "" or " " in hostname or hostname.startswith('.'):
            return False
        return True
    except Exception:
        return False

