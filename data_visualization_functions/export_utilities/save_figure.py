"""
Save a matplotlib figure to file.
"""

import logging
from pathlib import Path
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def save_figure(
    fig: Figure,
    filepath: str | Path,
    dpi: int = 300,
    bbox_inches: str = 'tight',
    transparent: bool = False,
) -> None:
    """
    Save a matplotlib figure to file.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure object to save.
    filepath : str | Path
        Output file path (extension determines format).
    dpi : int, optional
        Resolution in dots per inch (by default 300).
    bbox_inches : str, optional
        Bounding box specification (by default 'tight'):
        - 'tight': Tight bounding box
        - None: Standard bounding box
    transparent : bool, optional
        Whether to use transparent background (by default False).

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If dpi is invalid or filepath has no extension.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 9])
    >>> save_figure(fig, 'plot.png')

    >>> save_figure(fig, 'plot.pdf', dpi=600, transparent=True)

    Notes
    -----
    Supported formats: PNG, PDF, SVG, JPG, EPS, PS, TIFF.
    Format is automatically detected from file extension.

    Complexity
    ----------
    Time: O(n) where n is figure complexity, Space: O(n)
    """
    # Type validation
    if not isinstance(fig, Figure):
        raise TypeError(f"fig must be a Figure object, got {type(fig).__name__}")

    if not isinstance(filepath, (str, Path)):
        raise TypeError(
            f"filepath must be a string or Path, got {type(filepath).__name__}"
        )

    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")

    if bbox_inches is not None and not isinstance(bbox_inches, str):
        raise TypeError(
            f"bbox_inches must be a string or None, got {type(bbox_inches).__name__}"
        )

    if not isinstance(transparent, bool):
        raise TypeError(
            f"transparent must be a boolean, got {type(transparent).__name__}"
        )

    # Value validation
    if dpi < 1:
        raise ValueError(f"dpi must be positive, got {dpi}")

    filepath_obj = Path(filepath)

    if not filepath_obj.suffix:
        raise ValueError(f"filepath must have an extension (e.g., .png): '{filepath}'")

    valid_extensions = ['.png', '.pdf', '.svg', '.jpg', '.jpeg', '.eps', '.ps', '.tiff']
    if filepath_obj.suffix.lower() not in valid_extensions:
        logger.warning(
            f"Unusual file extension '{filepath_obj.suffix}'. "
            f"Supported: {valid_extensions}"
        )

    logger.debug(
        f"Saving figure to {filepath} with dpi={dpi}, "
        f"bbox_inches={bbox_inches}, transparent={transparent}"
    )

    # Create parent directory if it doesn't exist
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    fig.savefig(
        filepath_obj,
        dpi=dpi,
        bbox_inches=bbox_inches,
        transparent=transparent,
    )

    logger.info(f"Saved figure to {filepath_obj}")


__all__ = ['save_figure']
