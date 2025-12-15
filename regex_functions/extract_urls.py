"""
Extract URLs from text.
"""

import re


def extract_urls(
    text: str,
    unique: bool = True,
    include_schemes: list[str] | None = None,
) -> list[str]:
    """
    Extract all URLs from text.

    Parameters
    ----------
    text : str
        Input text to search for URLs.
    unique : bool, optional
        Return only unique URLs (by default True).
    include_schemes : list[str] | None, optional
        Filter URLs by schemes (e.g., ['http', 'https']).
        None means all schemes (by default None).

    Returns
    -------
    list[str]
        List of extracted URLs.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> text = "Visit https://example.com or http://test.org"
    >>> extract_urls(text)
    ['https://example.com', 'http://test.org']

    >>> text = "Links: ftp://files.com and https://site.com"
    >>> extract_urls(text, include_schemes=['https'])
    ['https://site.com']

    >>> text = "Same link: https://example.com and https://example.com"
    >>> extract_urls(text, unique=True)
    ['https://example.com']

    Notes
    -----
    Matches URLs with schemes (http, https, ftp, etc.).
    Does not validate if URL is reachable.

    Complexity
    ----------
    Time: O(n) where n is length of text
    Space: O(m) where m is number of URLs found
    """
    # Type validation
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not isinstance(unique, bool):
        raise TypeError(f"unique must be bool, got {type(unique).__name__}")
    if include_schemes is not None and not isinstance(include_schemes, list):
        raise TypeError(
            f"include_schemes must be list or None, got {type(include_schemes).__name__}"
        )

    # URL pattern with optional scheme
    pattern = r'(?:(?:https?|ftp|ftps|file)://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    
    # More specific pattern for URLs with schemes
    pattern_with_scheme = r'\b(?:https?|ftp|ftps|file)://[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    
    matches = re.findall(pattern_with_scheme, text)
    
    # Filter by schemes if specified
    if include_schemes is not None:
        filtered = []
        for url in matches:
            for scheme in include_schemes:
                if url.lower().startswith(f"{scheme.lower()}://"):
                    filtered.append(url)
                    break
        matches = filtered
    
    if unique:
        # Preserve order while removing duplicates
        seen = set()
        result = []
        for url in matches:
            if url not in seen:
                seen.add(url)
                result.append(url)
        return result
    
    return matches


__all__ = ['extract_urls']
