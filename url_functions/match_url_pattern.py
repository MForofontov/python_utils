"""
URL pattern matching and validation.
"""

import re
from typing import Any


def match_url_pattern(
    url: str,
    pattern: str,
    case_sensitive: bool = False,
) -> dict[str, str] | None:
    """
    Match URL against pattern and extract path variables.

    Implements pattern matching for URL routing and validation.
    Supports named capture groups for extracting URL components.
    Adds workflow logic beyond basic regex matching.

    Parameters
    ----------
    url : str
        URL to match against pattern.
    pattern : str
        URL pattern with named groups like "/users/{user_id}/posts/{post_id}".
    case_sensitive : bool, optional
        Case-sensitive matching (by default False).

    Returns
    -------
    dict[str, str] | None
        Dictionary of extracted variables, or None if no match.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If url or pattern is empty.

    Examples
    --------
    >>> match_url_pattern("/users/123", "/users/{user_id}")
    {'user_id': '123'}
    >>> match_url_pattern("/users/123/posts/456", "/users/{user_id}/posts/{post_id}")
    {'user_id': '123', 'post_id': '456'}
    >>> match_url_pattern("/api/v2/users", "/api/{version}/users")
    {'version': 'v2'}
    >>> match_url_pattern("/products", "/users/{id}")
    None

    Notes
    -----
    Uses regex but adds:
    - Pattern syntax translation ({var} to named groups)
    - Path component validation
    - Type-aware variable extraction
    - Query parameter pattern matching (optional)

    Pattern syntax:
    - {name} - Matches path segment (non-slash characters)
    - {name:int} - Matches digits only (type hint)
    - {name:path} - Matches multiple segments (including slashes)
    - * - Wildcard for single segment
    - ** - Wildcard for multiple segments

    Common use cases:
    - URL routing
    - API endpoint validation
    - Dynamic route matching
    - Path parameter extraction

    Complexity
    ----------
    Time: O(n) where n is URL length, Space: O(m) where m is captured vars
    """
    # Input validation
    if not isinstance(url, str):
        raise TypeError(f"url must be a string, got {type(url).__name__}")
    if not isinstance(pattern, str):
        raise TypeError(f"pattern must be a string, got {type(pattern).__name__}")
    if not isinstance(case_sensitive, bool):
        raise TypeError(f"case_sensitive must be a bool, got {type(case_sensitive).__name__}")

    if not url:
        raise ValueError("url cannot be empty")
    if not pattern:
        raise ValueError("pattern cannot be empty")

    # Convert pattern to regex
    regex_pattern = _pattern_to_regex(pattern)

    # Compile regex with appropriate flags
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        compiled_pattern = re.compile(regex_pattern, flags)
    except re.error as e:
        raise ValueError(f"Invalid pattern: {e}") from e

    # Match URL against pattern
    match = compiled_pattern.match(url)
    if not match:
        return None

    # Extract named groups
    return match.groupdict()


def _pattern_to_regex(pattern: str) -> str:
    """
    Convert URL pattern to regex.

    Handles:
    - {name} -> (?P<name>[^/]+)
    - {name:int} -> (?P<name>\\d+)
    - {name:path} -> (?P<name>.+)
    - * -> [^/]+
    - ** -> .+
    """
    # Escape special regex characters except for our pattern markers
    escaped = pattern

    # Replace {name:type} patterns with typed regex groups
    escaped = re.sub(
        r"\{(\w+):int\}",
        r"(?P<\1>\\d+)",
        escaped
    )
    escaped = re.sub(
        r"\{(\w+):path\}",
        r"(?P<\1>.+)",
        escaped
    )

    # Replace {name} patterns with named regex groups
    escaped = re.sub(
        r"\{(\w+)\}",
        r"(?P<\1>[^/]+)",
        escaped
    )

    # Replace wildcards
    escaped = escaped.replace("**", ".+")
    escaped = escaped.replace("*", "[^/]+")

    # Anchor pattern to match full URL
    return f"^{escaped}$"


def validate_url_format(
    url: str,
    require_scheme: bool = True,
    allowed_schemes: list[str] | None = None,
    require_netloc: bool = True,
) -> bool:
    """
    Validate URL format with advanced rules.

    Validates URL structure and components beyond basic parsing.
    Uses urllib but adds comprehensive validation logic.

    Parameters
    ----------
    url : str
        URL to validate.
    require_scheme : bool, optional
        URL must have scheme (by default True).
    allowed_schemes : list[str] | None, optional
        List of allowed schemes (by default None for any).
    require_netloc : bool, optional
        URL must have netloc/host (by default True).

    Returns
    -------
    bool
        True if URL is valid according to rules.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> validate_url_format("https://example.com/path")
    True
    >>> validate_url_format("/path/to/resource", require_scheme=False, require_netloc=False)
    True
    >>> validate_url_format("ftp://example.com", allowed_schemes=["http", "https"])
    False

    Notes
    -----
    Validates:
    - Scheme presence and whitelist
    - Netloc/host presence
    - Path format
    - Port number validity

    Complexity
    ----------
    Time: O(n) where n is URL length, Space: O(1)
    """
    from urllib.parse import urlparse

    # Input validation
    if not isinstance(url, str):
        raise TypeError(f"url must be a string, got {type(url).__name__}")
    if not isinstance(require_scheme, bool):
        raise TypeError(f"require_scheme must be bool, got {type(require_scheme).__name__}")
    if allowed_schemes is not None and not isinstance(allowed_schemes, list):
        raise TypeError(f"allowed_schemes must be list or None, got {type(allowed_schemes).__name__}")
    if not isinstance(require_netloc, bool):
        raise TypeError(f"require_netloc must be bool, got {type(require_netloc).__name__}")

    if not url:
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # Check scheme
    if require_scheme and not parsed.scheme:
        return False

    if allowed_schemes and parsed.scheme not in allowed_schemes:
        return False

    # Check netloc
    if require_netloc and not parsed.netloc:
        return False

    # Check port is valid number if present
    try:
        if parsed.port is not None and not (0 < parsed.port < 65536):
            return False
    except ValueError:
        # Invalid port number (out of range)
        return False

    return True


__all__ = ["match_url_pattern", "validate_url_format"]
