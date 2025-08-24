"""Simple HTTP GET request functionality."""

import urllib.request
import urllib.parse
from typing import Dict, Optional, Any
import json


def http_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
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
    ValueError
        If URL is invalid.
    urllib.error.URLError
        If the request fails.
        
    Examples
    --------
    >>> response = http_get('https://httpbin.org/get')
    >>> response['status_code']
    200
    >>> 'content' in response
    True
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    # Create request
    req = urllib.request.Request(url)
    
    # Add headers if provided
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode('utf-8')
            return {
                'status_code': response.getcode(),
                'content': content,
                'headers': dict(response.headers),
                'url': response.geturl()
            }
    except urllib.error.HTTPError as e:
        return {
            'status_code': e.code,
            'content': e.read().decode('utf-8') if e.fp else '',
            'headers': dict(e.headers) if e.headers else {},
            'url': url
        }
