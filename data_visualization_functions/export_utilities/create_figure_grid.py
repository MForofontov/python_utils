"""
Create a grid of subplots with figures.
"""

import logging
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def create_figure_grid(
    nrows: int,
    ncols: int,
    figsize: tuple[float, float] | None = None,
    **subplot_kw: Any,
) -> tuple[Figure, Any]:
    """
    Create a grid of subplots with figures.

    Parameters
    ----------
    nrows : int
        Number of rows in the grid.
    ncols : int
        Number of columns in the grid.
    figsize : tuple[float, float] | None, optional
        Figure size (width, height) in inches (by default None).
    **subplot_kw : Any
        Additional keyword arguments passed to plt.subplots.

    Returns
    -------
    tuple[Figure, Any]
        Tuple of (figure, axes):
        - figure: Figure object
        - axes: Array of Axes objects (or single Axes if 1x1)

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If nrows or ncols are invalid.

    Examples
    --------
    >>> fig, axes = create_figure_grid(2, 2, figsize=(10, 8))
    >>> axes[0, 0].plot([1, 2, 3])
    >>> axes[0, 1].scatter([1, 2], [3, 4])

    >>> fig, ax = create_figure_grid(1, 1, figsize=(8, 6))
    >>> ax.bar(['A', 'B'], [1, 2])

    Notes
    -----
    If nrows=ncols=1, returns a single Axes object instead of array.
    Use figsize to control overall figure dimensions.

    Complexity
    ----------
    Time: O(n*m) where n=rows, m=cols, Space: O(n*m)
    """
    # Type validation
    if not isinstance(nrows, int):
        raise TypeError(f"nrows must be an integer, got {type(nrows).__name__}")

    if not isinstance(ncols, int):
        raise TypeError(f"ncols must be an integer, got {type(ncols).__name__}")

    if figsize is not None:
        if not isinstance(figsize, tuple) or len(figsize) != 2:
            raise TypeError(
                f"figsize must be a tuple of two floats or None, got {type(figsize).__name__}"
            )

        if not all(isinstance(x, (int, float)) for x in figsize):
            raise TypeError("figsize values must be numeric")

    # Value validation
    if nrows < 1:
        raise ValueError(f"nrows must be positive, got {nrows}")

    if ncols < 1:
        raise ValueError(f"ncols must be positive, got {ncols}")

    if figsize is not None:
        if figsize[0] <= 0 or figsize[1] <= 0:
            raise ValueError(f"figsize values must be positive, got {figsize}")

    logger.debug(f"Creating figure grid: {nrows}x{ncols}, figsize={figsize}")

    # Create subplots
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        **subplot_kw,
    )

    logger.info(f"Created {nrows}x{ncols} figure grid")
    return fig, axes


__all__ = ["create_figure_grid"]
