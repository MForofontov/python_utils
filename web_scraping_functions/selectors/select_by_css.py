"""
Select elements using CSS selectors.
"""

from bs4 import BeautifulSoup, Tag


def select_by_css(
    element: BeautifulSoup | Tag,
    selector: str,
    limit: int | None = None,
) -> list[Tag]:
    """
    Select elements using CSS selector.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to search in.
    selector : str
        CSS selector string.
    limit : int | None, optional
        Maximum number of results (by default None).

    Returns
    -------
    list[Tag]
        List of matching elements.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If selector is empty or limit is non-positive.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '<div class="item">A</div><div class="item">B</div>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> elements = select_by_css(soup, "div.item")
    >>> len(elements)
    2

    >>> elements = select_by_css(soup, "div.item", limit=1)
    >>> len(elements)
    1

    Notes
    -----
    Supports all CSS3 selectors.

    Complexity
    ----------
    Time: O(n), Space: O(m), where n is element size, m is matching elements
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(selector, str):
        raise TypeError(f"selector must be a string, got {type(selector).__name__}")
    if limit is not None and not isinstance(limit, int):
        raise TypeError(f"limit must be an integer or None, got {type(limit).__name__}")
    
    if not selector.strip():
        raise ValueError("selector cannot be empty")
    
    if limit is not None and limit <= 0:
        raise ValueError(f"limit must be positive, got {limit}")
    
    if limit is not None:
        results = element.select(selector, limit=limit)
    else:
        results = element.select(selector)
    return results


__all__ = ['select_by_css']
