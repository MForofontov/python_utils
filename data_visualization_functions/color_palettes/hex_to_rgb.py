"""
Convert hex color code to RGB tuple.
"""

import logging

logger = logging.getLogger(__name__)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convert hex color code to RGB tuple.

    Parameters
    ----------
    hex_color : str
        Hex color code (e.g., '#FF0000' or 'FF0000').

    Returns
    -------
    tuple[int, int, int]
        RGB values as integers (0-255).

    Raises
    ------
    TypeError
        If hex_color is not a string.
    ValueError
        If hex_color is not a valid hex code.

    Examples
    --------
    >>> hex_to_rgb('#FF0000')
    (255, 0, 0)

    >>> hex_to_rgb('00FF00')
    (0, 255, 0)

    Notes
    -----
    Accepts hex codes with or without the leading '#' symbol.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(hex_color, str):
        raise TypeError(f"hex_color must be a string, got {type(hex_color).__name__}")

    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Value validation
    if len(hex_color) != 6:
        raise ValueError(f"hex_color must be 6 characters (excluding #), got '{hex_color}'")

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError as e:
        raise ValueError(f"Invalid hex color code '{hex_color}': {e}") from e

    logger.debug(f"Converted {hex_color} to RGB({r}, {g}, {b})")
    return (r, g, b)


__all__ = ['hex_to_rgb']
