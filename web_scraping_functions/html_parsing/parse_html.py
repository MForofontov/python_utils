"""
Parse HTML content using BeautifulSoup.
"""

from bs4 import BeautifulSoup


def parse_html(
    html: str,
    parser: str = "html.parser",
) -> BeautifulSoup:
    """
    Parse HTML content into a BeautifulSoup object.

    Parameters
    ----------
    html : str
        HTML content to parse.
    parser : str, optional
        Parser to use (by default "html.parser").
        Options: "html.parser", "lxml", "html5lib", "xml".

    Returns
    -------
    BeautifulSoup
        Parsed HTML object.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If html is empty or parser is invalid.

    Examples
    --------
    >>> html = "<html><body><p>Hello</p></body></html>"
    >>> soup = parse_html(html)
    >>> soup.find('p').text
    'Hello'

    >>> soup = parse_html(html, parser="lxml")
    >>> soup.name
    '[document]'

    Notes
    -----
    Different parsers have different behaviors:
    - html.parser: Built-in, no dependencies
    - lxml: Fast, requires lxml package
    - html5lib: Most lenient, requires html5lib package
    - xml: For XML documents, requires lxml package

    Complexity
    ----------
    Time: O(n), Space: O(n), where n is HTML length
    """
    if not isinstance(html, str):
        raise TypeError(f"html must be a string, got {type(html).__name__}")
    if not isinstance(parser, str):
        raise TypeError(f"parser must be a string, got {type(parser).__name__}")
    
    if not html.strip():
        raise ValueError("html cannot be empty")
    
    valid_parsers = {"html.parser", "lxml", "html5lib", "xml"}
    if parser not in valid_parsers:
        raise ValueError(f"parser must be one of {valid_parsers}, got {parser}")
    
    return BeautifulSoup(html, parser)


__all__ = ['parse_html']
