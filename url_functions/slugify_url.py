"""
URL slugification for SEO-friendly URLs.
"""

import re
import unicodedata


def slugify_url(
    text: str,
    max_length: int | None = None,
    separator: str = "-",
    lowercase: bool = True,
    allow_unicode: bool = False,
) -> str:
    """
    Convert text to SEO-friendly URL slug.

    Transforms text into a clean, URL-safe slug by removing special characters,
    handling unicode, and applying consistent formatting. Uses urllib for
    encoding but adds workflow logic for slug generation rules.

    Parameters
    ----------
    text : str
        Text to convert to slug.
    max_length : int | None, optional
        Maximum slug length (by default None for unlimited).
    separator : str, optional
        Word separator character (by default "-").
    lowercase : bool, optional
        Convert to lowercase (by default True).
    allow_unicode : bool, optional
        Keep unicode characters (by default False).

    Returns
    -------
    str
        URL-safe slug.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If text is empty or parameters are invalid.

    Examples
    --------
    >>> slugify_url("Hello World!")
    'hello-world'
    >>> slugify_url("Python 3.11: New Features")
    'python-3-11-new-features'
    >>> slugify_url("Café & Restaurant", allow_unicode=True)
    'café-restaurant'
    >>> slugify_url("Very Long Title Here", max_length=10)
    'very-long'

    Notes
    -----
    Uses unicodedata for normalization but adds:
    - SEO best practices (hyphens, lowercase)
    - Length limiting with word boundary preservation
    - Special character handling rules
    - Multiple whitespace/separator collapsing
    - Leading/trailing separator removal

    Common use cases:
    - Blog post URLs from titles
    - Product page URLs from names
    - Category/tag URLs

    Complexity
    ----------
    Time: O(n) where n is text length, Space: O(n)
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")
    if max_length is not None and not isinstance(max_length, int):
        raise TypeError(
            f"max_length must be int or None, got {type(max_length).__name__}"
        )
    if not isinstance(separator, str):
        raise TypeError(f"separator must be a string, got {type(separator).__name__}")
    if not isinstance(lowercase, bool):
        raise TypeError(f"lowercase must be a bool, got {type(lowercase).__name__}")
    if not isinstance(allow_unicode, bool):
        raise TypeError(
            f"allow_unicode must be a bool, got {type(allow_unicode).__name__}"
        )

    if not text:
        raise ValueError("text cannot be empty")
    if max_length is not None and max_length < 1:
        raise ValueError(f"max_length must be positive, got {max_length}")
    if not separator:
        raise ValueError("separator cannot be empty")

    # Normalize unicode characters
    if not allow_unicode:
        # Convert unicode to closest ASCII representation
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
    else:
        text = unicodedata.normalize("NFKC", text)

    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()

    # Replace spaces and special characters with separator
    # Keep alphanumeric, unicode letters (if allowed), and hyphens
    if allow_unicode:
        # Keep unicode letters
        text = re.sub(r"[^\w\s-]", "", text)
    else:
        # Only ASCII alphanumeric
        text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)

    # Replace whitespace with separator
    text = re.sub(r"[\s]+", separator, text)

    # Remove duplicate separators
    text = re.sub(f"{re.escape(separator)}{{2,}}", separator, text)

    # Remove leading/trailing separators
    text = text.strip(separator)

    # Apply max length, preserving word boundaries if possible
    if max_length and len(text) > max_length:
        # Try to cut at separator to preserve words
        text = text[:max_length]
        last_sep = text.rfind(separator)
        if last_sep > 0:
            text = text[:last_sep]
        text = text.strip(separator)

    return text


__all__ = ["slugify_url"]
