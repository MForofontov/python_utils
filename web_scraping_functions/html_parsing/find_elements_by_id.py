"""
Find HTML element by ID.
"""

from bs4 import BeautifulSoup, Tag


def find_elements_by_id(
    element: BeautifulSoup | Tag,
    element_id: str,
) -> Tag | None:
    """
    Find element with specified ID.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to search in.
    element_id : str
        ID to search for.

    Returns
    -------
    Tag | None
        Matching element or None if not found.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If element_id is empty.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '<div id="main">Content</div>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> elem = find_elements_by_id(soup, "main")
    >>> elem.get_text()
    'Content'

    >>> elem = find_elements_by_id(soup, "nonexistent")
    >>> elem is None
    True

    Notes
    -----
    IDs should be unique in valid HTML.

    Complexity
    ----------
    Time: O(n), Space: O(1), where n is element size
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(element_id, str):
        raise TypeError(f"element_id must be a string, got {type(element_id).__name__}")
    
    if not element_id.strip():
        raise ValueError("element_id cannot be empty")
    
    return element.find(id=element_id)


__all__ = ['find_elements_by_id']
