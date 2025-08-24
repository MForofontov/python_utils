"""Domain extraction functionality."""

import urllib.parse
from typing import Optional
from .validate_url import is_valid_url


def extract_domain(url: str) -> Optional[str]:
    """
    Extract the domain from a URL.
    
    Parameters
    ----------
    url : str
        The URL to extract the domain from.
        
    Returns
    -------
    str or None
        The domain name, or None if the URL is invalid.
        
    Examples
    --------
    >>> extract_domain('https://www.example.com/path')
    'www.example.com'
    >>> extract_domain('invalid-url')
    None
    """
    if not is_valid_url(url):
        return None
    
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname
