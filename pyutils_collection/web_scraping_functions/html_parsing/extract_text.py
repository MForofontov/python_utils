"""
Extract text content from HTML elements.
"""

from bs4 import BeautifulSoup, Tag


def extract_text(
    element: BeautifulSoup | Tag,
    strip: bool = True,
    separator: str = " ",
) -> str:
    """
    Extract text content from HTML element.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to extract text from.
    strip : bool, optional
        Whether to strip whitespace (by default True).
    separator : str, optional
        Separator for joining text (by default " ").

    Returns
    -------
    str
        Extracted text content.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = "<div>  Hello  <span>World</span>  </div>"
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> extract_text(soup)
    'Hello World'

    >>> extract_text(soup, strip=False)
    '  Hello  World  '

    >>> extract_text(soup, separator="-")
    'Hello-World'

    Notes
    -----
    Text extraction preserves the order of elements and
    can handle nested tags.

    Complexity
    ----------
    Time: O(n), Space: O(n), where n is element size
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(strip, bool):
        raise TypeError(f"strip must be a boolean, got {type(strip).__name__}")
    if not isinstance(separator, str):
        raise TypeError(f"separator must be a string, got {type(separator).__name__}")

    if strip:
        return element.get_text(separator=separator, strip=True)
    return element.get_text(separator=separator)


__all__ = ["extract_text"]
