"""
Set default figure size and DPI for all subsequent plots.
"""

import logging

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def set_figure_size(
    width: float,
    height: float,
    dpi: int = 100,
) -> None:
    """
    Set default figure size and DPI for all subsequent plots.

    Parameters
    ----------
    width : float
        Figure width in inches.
    height : float
        Figure height in inches.
    dpi : int, optional
        Dots per inch for figure resolution (by default 100).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> set_figure_size(12, 8, dpi=150)
    >>> # All subsequent plots will be 12x8 inches at 150 DPI

    >>> set_figure_size(8, 6)
    >>> # Back to smaller size

    Notes
    -----
    This affects the default size for all new figures created after calling
    this function. Existing figures are not modified.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(width, (int, float)):
        raise TypeError(f"width must be a number, got {type(width).__name__}")
    if not isinstance(height, (int, float)):
        raise TypeError(f"height must be a number, got {type(height).__name__}")
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")

    # Value validation
    if width <= 0:
        raise ValueError(f"width must be positive, got {width}")
    if height <= 0:
        raise ValueError(f"height must be positive, got {height}")
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")

    plt.rcParams["figure.figsize"] = (width, height)
    plt.rcParams["figure.dpi"] = dpi

    logger.info(f"Set default figure size to {width}x{height} inches at {dpi} DPI")


__all__ = ["set_figure_size"]
