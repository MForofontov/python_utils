"""
Generate a colorblind-safe color palette.
"""

import logging

logger = logging.getLogger(__name__)


def get_colorblind_safe_palette(n_colors: int) -> list[str]:
    """
    Generate a colorblind-safe color palette.

    Parameters
    ----------
    n_colors : int
        Number of colors needed.

    Returns
    -------
    list[str]
        List of colorblind-safe hex color codes.

    Raises
    ------
    TypeError
        If n_colors is not an integer.
    ValueError
        If n_colors is not positive or exceeds maximum available colors.

    Examples
    --------
    >>> colors = get_colorblind_safe_palette(5)
    >>> len(colors)
    5

    >>> colors = get_colorblind_safe_palette(8)
    >>> # All colors are distinguishable for colorblind viewers

    Notes
    -----
    Uses Paul Tol's colorblind-safe color schemes. Maximum 12 colors available.
    For more colors, consider using different markers or line styles.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(n_colors, int):
        raise TypeError(f"n_colors must be an integer, got {type(n_colors).__name__}")

    # Value validation
    if n_colors <= 0:
        raise ValueError(f"n_colors must be positive, got {n_colors}")

    # Paul Tol's colorblind-safe palette
    colorblind_safe = [
        '#4477AA',  # Blue
        '#EE6677',  # Red
        '#228833',  # Green
        '#CCBB44',  # Yellow
        '#66CCEE',  # Cyan
        '#AA3377',  # Purple
        '#BBBBBB',  # Grey
        '#EE7733',  # Orange
        '#009988',  # Teal
        '#CC3311',  # Dark red
        '#33BBEE',  # Light blue
        '#EE3377',  # Magenta
    ]

    if n_colors > len(colorblind_safe):
        raise ValueError(
            f"n_colors ({n_colors}) exceeds maximum colorblind-safe colors ({len(colorblind_safe)}). "
            "Consider using different markers or line styles for additional distinction."
        )

    colors = colorblind_safe[:n_colors]
    logger.debug(f"Retrieved {n_colors} colorblind-safe colors")
    return colors


__all__ = ['get_colorblind_safe_palette']
