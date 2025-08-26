"""Simple HTTP POST request functionality."""

import urllib.request
from urllib.error import HTTPError, URLError
from typing import Dict, Optional, Any, Union
import json


def http_post(url: str, data: Optional[Union[Dict[str, Any], str]] = None, 
              headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
    """
    Perform a simple HTTP POST request.
    
    Parameters
    ----------
    url : str
        The URL to send the POST request to.
    data : dict or str, optional
        Data to send in the POST request. If dict, will be JSON encoded.
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
        If URL is not a string.
    ValueError
        If URL is an empty string.
    URLError
        If the request fails.
        
    Examples
    --------
    >>> response = http_post('https://httpbin.org/post', {'key': 'value'})
    >>> response['status_code']
    200
    >>> 'content' in response
    True
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    if not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    # Prepare data
    if data is not None:
        if isinstance(data, dict):
            post_data = json.dumps(data).encode('utf-8')
            content_type = 'application/json'
        else:
            post_data = data.encode('utf-8') if isinstance(data, str) else data
            content_type = 'application/x-www-form-urlencoded'
    else:
        post_data = None
        content_type = None
    
    # Create request
    req = urllib.request.Request(url, data=post_data)
    
    # Set content type if we have data
    if content_type:
        req.add_header('Content-Type', content_type)
    
    # Add additional headers if provided
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
    except HTTPError as e:
        return {
            'status_code': e.code,
            'content': e.read().decode('utf-8') if e.fp else '',
            'headers': dict(e.headers) if e.headers else {},
            'url': url
        }
    except URLError as e:
        raise URLError(f"Failed to reach {url}: {e.reason}") from e
