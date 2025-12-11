"""
Find HTML elements by class name.
"""

from bs4 import BeautifulSoup, Tag


def find_elements_by_class(
    element: BeautifulSoup | Tag,
    class_name: str,
    limit: int | None = None,
) -> list[Tag]:
    """
    Find all elements with specified class name.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to search in.
    class_name : str
        Class name to search for.
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
        If class_name is empty or limit is non-positive.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '<div class="item">A</div><div class="item">B</div>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> elements = find_elements_by_class(soup, "item")
    >>> len(elements)
    2

    >>> elements = find_elements_by_class(soup, "item", limit=1)
    >>> len(elements)
    1

    Notes
    -----
    Supports multiple classes on same element.

    Complexity
    ----------
    Time: O(n), Space: O(m), where n is element size, m is matching elements
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(class_name, str):
        raise TypeError(f"class_name must be a string, got {type(class_name).__name__}")
    if limit is not None and not isinstance(limit, int):
        raise TypeError(f"limit must be an integer or None, got {type(limit).__name__}")
    
    if not class_name.strip():
        raise ValueError("class_name cannot be empty")
    
    if limit is not None and limit <= 0:
        raise ValueError(f"limit must be positive, got {limit}")
    
    return element.find_all(class_=class_name, limit=limit)


__all__ = ['find_elements_by_class']
