"""
Adjust the brightness of a color.
"""

import logging
from matplotlib.colors import to_rgb, to_hex

logger = logging.getLogger(__name__)


def adjust_brightness(color: str, factor: float) -> str:
    """
    Adjust the brightness of a color.

    Parameters
    ----------
    color : str
        Color specification (name or hex code).
    factor : float
        Brightness adjustment factor:
        - factor > 1.0: lighter
        - factor < 1.0: darker
        - factor = 1.0: no change

    Returns
    -------
    str
        Adjusted color as hex code.

    Raises
    ------
    TypeError
        If color is not a string or factor is not numeric.
    ValueError
        If color is invalid or factor is non-positive.

    Examples
    --------
    >>> adjust_brightness('red', 0.5)
    '#800000'

    >>> adjust_brightness('#FF0000', 1.5)
    '#FF8080'

    Notes
    -----
    Uses linear interpolation in RGB space. Values are clamped to [0, 1].

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(color, str):
        raise TypeError(f"color must be a string, got {type(color).__name__}")
    if not isinstance(factor, (int, float)):
        raise TypeError(f"factor must be numeric, got {type(factor).__name__}")

    # Value validation
    if factor <= 0:
        raise ValueError(f"factor must be positive, got {factor}")

    try:
        r, g, b = to_rgb(color)
    except ValueError as e:
        raise ValueError(f"Invalid color specification '{color}': {e}") from e

    # Adjust brightness
    if factor > 1.0:
        # Lighten: interpolate toward white
        r = r + (1.0 - r) * (factor - 1.0) / factor
        g = g + (1.0 - g) * (factor - 1.0) / factor
        b = b + (1.0 - b) * (factor - 1.0) / factor
    else:
        # Darken: scale down
        r *= factor
        g *= factor
        b *= factor

    # Clamp to [0, 1]
    r = max(0.0, min(1.0, r))
    g = max(0.0, min(1.0, g))
    b = max(0.0, min(1.0, b))

    adjusted_color = to_hex((r, g, b), keep_alpha=False)
    logger.debug(f"Adjusted brightness of {color} by {factor}: {adjusted_color}")
    return adjusted_color


__all__ = ['adjust_brightness']
