"""
Remove extra whitespace from text.
"""

import re


def remove_extra_whitespace(
    text: str,
    preserve_newlines: bool = False,
) -> str:
    """
    Remove extra whitespace from text.

    Parameters
    ----------
    text : str
        Input text with potential extra whitespace.
    preserve_newlines : bool, optional
        Keep newline characters (by default False).

    Returns
    -------
    str
        Text with normalized whitespace.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> text = "Hello    world   !"
    >>> remove_extra_whitespace(text)
    'Hello world !'

    >>> text = "Line1\\n\\n\\nLine2"
    >>> remove_extra_whitespace(text)
    'Line1 Line2'

    >>> text = "Line1\\n\\n\\nLine2"
    >>> remove_extra_whitespace(text, preserve_newlines=True)
    'Line1\\nLine2'

    >>> text = "  Multiple   spaces  "
    >>> remove_extra_whitespace(text)
    'Multiple spaces'

    Notes
    -----
    Normalizes:
    - Multiple spaces to single space
    - Multiple newlines to single newline (if preserve_newlines=True)
    - Tabs to spaces
    - Removes leading/trailing whitespace

    Complexity
    ----------
    Time: O(n) where n is length of text
    Space: O(n) for result string
    """
    # Type validation
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not isinstance(preserve_newlines, bool):
        raise TypeError(
            f"preserve_newlines must be bool, got {type(preserve_newlines).__name__}"
        )

    if preserve_newlines:
        # Replace multiple newlines with single newline
        text = re.sub(r"\n\s*\n+", "\n", text)
        # Replace multiple spaces/tabs with single space (but not newlines)
        text = re.sub(r"[^\S\n]+", " ", text)
        # Strip each line
        lines = text.split("\n")
        text = "\n".join(line.strip() for line in lines)
    else:
        # Replace all whitespace (including newlines) with single space
        text = re.sub(r"\s+", " ", text)
        # Strip leading and trailing whitespace
        text = text.strip()

    return text


__all__ = ["remove_extra_whitespace"]
