"""Query parameters extraction functionality."""

import urllib.parse


def get_query_params(url: str) -> dict[str, list[str]]:
    """
    Extract query parameters from a URL.
    
    Parameters
    ----------
    url : str
        The URL to extract query parameters from.
        
    Returns
    -------
    dict
        Dictionary of query parameters with lists of values.
        
    Raises
    ------
    ValueError
        If URL is invalid.
        
    Examples
    --------
    >>> get_query_params('https://example.com?q=search&page=1&tag=python&tag=web')
    {'q': ['search'], 'page': ['1'], 'tag': ['python', 'web']}
    >>> get_query_params('https://example.com')
    {}
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(parsed.query)
