"""URL validation functionality."""

import urllib.parse
from typing import Optional, List


def is_valid_url(url: str, allowed_schemes: Optional[List[str]] = None) -> bool:
    """
    Validate if a string is a valid URL.
    
    Parameters
    ----------
    url : str
        The URL to validate.
    allowed_schemes : list of str, optional
        List of allowed schemes (e.g., ['http', 'https']). If None, all schemes are allowed.
        
    Returns
    -------
    bool
        True if the URL is valid, False otherwise.
        
    Examples
    --------
    >>> is_valid_url('https://example.com')
    True
    >>> is_valid_url('not-a-url')
    False
    >>> is_valid_url('ftp://example.com', ['http', 'https'])
    False
    """
    if not isinstance(url, str) or not url.strip():
        return False
    
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Check if we have a scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Check allowed schemes if provided
        if allowed_schemes and parsed.scheme not in allowed_schemes:
            return False
        
        # Additional validation: hostname should not be empty
        if not parsed.hostname:
            return False
        
        return True
    except Exception:
        return False
