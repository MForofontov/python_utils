"""
Extract next page URL from HTML.
"""

from bs4 import BeautifulSoup, Tag


def extract_next_page(
    element: BeautifulSoup | Tag,
    selector: str = "a[rel='next']",
    attribute: str = "href",
) -> str | None:
    """
    Extract next page URL from HTML element.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to search in.
    selector : str, optional
        CSS selector for next link (by default "a[rel='next']").
    attribute : str, optional
        Attribute containing URL (by default "href").

    Returns
    -------
    str | None
        Next page URL or None if not found.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If selector or attribute is empty.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '<a rel="next" href="/page2">Next</a>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> extract_next_page(soup)
    '/page2'

    >>> html = '<a class="next-btn" href="/page3">Next</a>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> extract_next_page(soup, selector="a.next-btn")
    '/page3'

    Notes
    -----
    Returns None if no next page link is found.

    Complexity
    ----------
    Time: O(n), Space: O(1), where n is element size
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(selector, str):
        raise TypeError(f"selector must be a string, got {type(selector).__name__}")
    if not isinstance(attribute, str):
        raise TypeError(f"attribute must be a string, got {type(attribute).__name__}")
    
    if not selector.strip():
        raise ValueError("selector cannot be empty")
    
    if not attribute.strip():
        raise ValueError("attribute cannot be empty")
    
    next_link = element.select_one(selector)
    if next_link and next_link.has_attr(attribute):
        return next_link[attribute]  # type: ignore[return-value]
    
    return None


__all__ = ['extract_next_page']
