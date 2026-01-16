"""
Remove HTML tags from text.
"""

import re


def remove_html_tags(
    text: str,
    keep_text: bool = True,
) -> str:
    """
    Remove HTML/XML tags from text.

    Parameters
    ----------
    text : str
        Input text containing HTML/XML tags.
    keep_text : bool, optional
        Keep text content between tags (by default True).

    Returns
    -------
    str
        Text with HTML tags removed.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> html = "<p>Hello <b>world</b>!</p>"
    >>> remove_html_tags(html)
    'Hello world!'

    >>> html = "<div><span>Text</span></div>"
    >>> remove_html_tags(html, keep_text=True)
    'Text'

    >>> html = "<!-- Comment --><p>Content</p>"
    >>> remove_html_tags(html)
    'Content'

    Notes
    -----
    Removes:
    - HTML/XML tags (<tag>...</tag>)
    - Self-closing tags (<tag />)
    - Comments (<!-- ... -->)
    - CDATA sections (<![CDATA[...]]>)

    Does not parse HTML structure, uses regex.

    Complexity
    ----------
    Time: O(n) where n is length of text
    Space: O(n) for result string
    """
    # Type validation
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not isinstance(keep_text, bool):
        raise TypeError(f"keep_text must be bool, got {type(keep_text).__name__}")

    # Remove comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Remove CDATA sections
    text = re.sub(r"<!\[CDATA\[.*?\]\]>", "", text, flags=re.DOTALL)

    # Remove script and style tags with their content
    text = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove all other HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    if keep_text:
        # Clean up extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

    return text


__all__ = ["remove_html_tags"]
