"""
Convert RGB tuple to hex color code.
"""

import logging

logger = logging.getLogger(__name__)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB tuple to hex color code.

    Parameters
    ----------
    r : int
        Red value (0-255).
    g : int
        Green value (0-255).
    b : int
        Blue value (0-255).

    Returns
    -------
    str
        Hex color code with leading '#'.

    Raises
    ------
    TypeError
        If r, g, or b are not integers.
    ValueError
        If r, g, or b are outside the 0-255 range.

    Examples
    --------
    >>> rgb_to_hex(255, 0, 0)
    '#FF0000'

    >>> rgb_to_hex(0, 128, 255)
    '#0080FF'

    Notes
    -----
    Returns uppercase hex codes with leading '#' symbol.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(r, int):
        raise TypeError(f"r must be an integer, got {type(r).__name__}")
    if not isinstance(g, int):
        raise TypeError(f"g must be an integer, got {type(g).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    # Value validation
    if not 0 <= r <= 255:
        raise ValueError(f"r must be in range [0, 255], got {r}")
    if not 0 <= g <= 255:
        raise ValueError(f"g must be in range [0, 255], got {g}")
    if not 0 <= b <= 255:
        raise ValueError(f"b must be in range [0, 255], got {b}")

    hex_color = f"#{r:02X}{g:02X}{b:02X}"
    logger.debug(f"Converted RGB({r}, {g}, {b}) to {hex_color}")
    return hex_color


__all__ = ['rgb_to_hex']
