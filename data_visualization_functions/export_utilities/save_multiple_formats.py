"""
Save a figure in multiple formats.
"""

import logging
from pathlib import Path
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def save_multiple_formats(
    fig: Figure,
    base_filepath: str | Path,
    formats: list[str] | None = None,
    dpi: int = 300,
    transparent: bool = False,
) -> list[Path]:
    """
    Save a figure in multiple formats.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure object to save.
    base_filepath : str | Path
        Base output path (without extension).
    formats : list[str] | None, optional
        List of formats to save (by default ['png', 'pdf', 'svg']).
    dpi : int, optional
        Resolution in dots per inch (by default 300).
    transparent : bool, optional
        Whether to use transparent background (by default False).

    Returns
    -------
    list[Path]
        List of paths to saved files.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If formats is empty or contains invalid values.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 9])
    >>> paths = save_multiple_formats(fig, 'output/plot')
    >>> len(paths)
    3

    >>> paths = save_multiple_formats(fig, 'plot', formats=['png', 'pdf'], dpi=600)
    >>> all(p.exists() for p in paths)
    True

    Notes
    -----
    Supported formats: png, pdf, svg, jpg, eps.
    Creates output directory if it doesn't exist.

    Complexity
    ----------
    Time: O(n*m) where n=figure complexity, m=formats, Space: O(n*m)
    """
    # Type validation
    if not isinstance(fig, Figure):
        raise TypeError(f"fig must be a Figure object, got {type(fig).__name__}")

    if not isinstance(base_filepath, (str, Path)):
        raise TypeError(
            f"base_filepath must be a string or Path, got {type(base_filepath).__name__}"
        )

    if formats is not None and not isinstance(formats, list):
        raise TypeError(f"formats must be a list or None, got {type(formats).__name__}")

    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")

    if not isinstance(transparent, bool):
        raise TypeError(
            f"transparent must be a boolean, got {type(transparent).__name__}"
        )

    # Value validation
    if dpi < 1:
        raise ValueError(f"dpi must be positive, got {dpi}")

    # Default formats
    if formats is None:
        formats = ['png', 'pdf', 'svg']

    if not formats:
        raise ValueError("formats list cannot be empty")

    valid_formats = ['png', 'pdf', 'svg', 'jpg', 'jpeg', 'eps', 'ps', 'tiff']
    for fmt in formats:
        if not isinstance(fmt, str):
            raise TypeError(f"format must be a string, got {type(fmt).__name__}")

        if fmt.lower() not in valid_formats:
            raise ValueError(
                f"Invalid format '{fmt}', must be one of {valid_formats}"
            )

    logger.debug(
        f"Saving figure to multiple formats {formats} with dpi={dpi}"
    )

    # Prepare base path
    base_path = Path(base_filepath)

    # Remove extension if present
    if base_path.suffix:
        base_path = base_path.with_suffix('')

    # Create parent directory
    base_path.parent.mkdir(parents=True, exist_ok=True)

    # Save in each format
    saved_paths = []

    for fmt in formats:
        output_path = base_path.with_suffix(f'.{fmt.lower()}')

        fig.savefig(
            output_path,
            dpi=dpi,
            bbox_inches='tight',
            transparent=transparent,
        )

        saved_paths.append(output_path)
        logger.info(f"Saved figure to {output_path}")

    logger.info(f"Saved figure in {len(saved_paths)} formats")
    return saved_paths


__all__ = ['save_multiple_formats']
