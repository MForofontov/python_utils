"""
Extract attribute values from elements.
"""

from bs4 import Tag


def extract_attribute(
    element: Tag,
    attribute: str,
    default: str | None = None,
) -> str | None:
    """
    Extract attribute value from HTML element.

    Parameters
    ----------
    element : Tag
        HTML element.
    attribute : str
        Attribute name to extract.
    default : str | None, optional
        Default value if attribute not found (by default None).

    Returns
    -------
    str | None
        Attribute value or default.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If attribute is empty.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '<a href="/page" class="link">Click</a>'
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> link = soup.find('a')
    >>> extract_attribute(link, 'href')
    '/page'

    >>> extract_attribute(link, 'class')
    ['link']

    >>> extract_attribute(link, 'id', default='no-id')
    'no-id'

    Notes
    -----
    Some attributes like 'class' return lists.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(element, Tag):
        raise TypeError(f"element must be a Tag, got {type(element).__name__}")
    if not isinstance(attribute, str):
        raise TypeError(f"attribute must be a string, got {type(attribute).__name__}")
    if default is not None and not isinstance(default, str):
        raise TypeError(
            f"default must be a string or None, got {type(default).__name__}"
        )

    if not attribute.strip():
        raise ValueError("attribute cannot be empty")

    return element.get(attribute, default)  # type: ignore[return-value]


__all__ = ["extract_attribute"]
