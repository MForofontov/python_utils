"""
Select elements using XPath selectors.
"""

from lxml import etree
from lxml import html as lxml_html


def select_by_xpath(
    html: str,
    xpath: str,
) -> list[etree._Element]:
    """
    Select elements using XPath selector.

    Parameters
    ----------
    html : str
        HTML content to parse.
    xpath : str
        XPath selector string.

    Returns
    -------
    list[etree._Element]
        List of matching elements.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If html or xpath is empty.

    Examples
    --------
    >>> html = '<div><p class="text">Hello</p><p class="text">World</p></div>'
    >>> elements = select_by_xpath(html, '//p[@class="text"]')
    >>> len(elements)
    2

    >>> elements = select_by_xpath(html, '//p[@class="text"][1]')
    >>> len(elements)
    1

    Notes
    -----
    Uses lxml library for XPath support.
    Returns lxml Element objects, not BeautifulSoup Tags.

    Complexity
    ----------
    Time: O(n), Space: O(m), where n is HTML size, m is matching elements
    """
    if not isinstance(html, str):
        raise TypeError(f"html must be a string, got {type(html).__name__}")
    if not isinstance(xpath, str):
        raise TypeError(f"xpath must be a string, got {type(xpath).__name__}")

    if not html.strip():
        raise ValueError("html cannot be empty")

    if not xpath.strip():
        raise ValueError("xpath cannot be empty")

    tree = lxml_html.fromstring(html)
    elements = tree.xpath(xpath)

    # Ensure we return a list
    if not isinstance(elements, list):
        elements = [elements]

    return elements


__all__ = ["select_by_xpath"]
