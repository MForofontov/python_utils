"""
Export utilities for saving visualizations in various formats.

This module provides utilities for exporting matplotlib and plotly figures
to different file formats with comprehensive configuration options.
"""

import logging
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def save_figure(
    fig: Figure,
    filepath: str | Path,
    format: Literal['png', 'svg', 'pdf', 'jpg', 'eps'] | None = None,
    dpi: int = 300,
    transparent: bool = False,
    bbox_inches: str | None = 'tight',
    pad_inches: float = 0.1,
) -> None:
    """
    Save a matplotlib figure to a file with comprehensive options.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure to save.
    filepath : str | Path
        Output file path.
    format : Literal['png', 'svg', 'pdf', 'jpg', 'eps'] | None, optional
        Output format. If None, inferred from filepath extension (by default None).
    dpi : int, optional
        Resolution in dots per inch for raster formats (by default 300).
    transparent : bool, optional
        Whether to use transparent background (by default False).
    bbox_inches : str | None, optional
        Bounding box in inches. Use 'tight' to minimize whitespace (by default 'tight').
    pad_inches : float, optional
        Padding around the figure when bbox_inches is 'tight' (by default 0.1).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values or file cannot be created.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 2])
    >>> save_figure(fig, 'plot.png', dpi=300)

    >>> # Save as vector format
    >>> save_figure(fig, 'plot.svg', transparent=True)

    >>> # High-resolution PDF
    >>> save_figure(fig, 'plot.pdf', dpi=600)

    Notes
    -----
    Vector formats (SVG, PDF, EPS) are scalable and ideal for publications.
    Raster formats (PNG, JPG) have fixed resolution determined by DPI.

    Complexity
    ----------
    Time: O(n) where n is figure complexity, Space: O(1)
    """
    # Type validation
    if not isinstance(fig, Figure):
        raise TypeError(f"fig must be a matplotlib Figure, got {type(fig).__name__}")
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"filepath must be a string or Path, got {type(filepath).__name__}")
    if format is not None and not isinstance(format, str):
        raise TypeError(f"format must be a string or None, got {type(format).__name__}")
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")
    if not isinstance(transparent, bool):
        raise TypeError(f"transparent must be a boolean, got {type(transparent).__name__}")
    if bbox_inches is not None and not isinstance(bbox_inches, str):
        raise TypeError(f"bbox_inches must be a string or None, got {type(bbox_inches).__name__}")
    if not isinstance(pad_inches, (int, float)):
        raise TypeError(f"pad_inches must be a number, got {type(pad_inches).__name__}")

    # Value validation
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")
    if pad_inches < 0:
        raise ValueError(f"pad_inches must be non-negative, got {pad_inches}")

    # Convert to Path
    filepath = Path(filepath)

    # Determine format
    if format is None:
        format_str = filepath.suffix.lstrip('.')
        if not format_str:
            raise ValueError("Cannot determine format from filepath without extension")
    else:
        format_str = format

    valid_formats = ['png', 'svg', 'pdf', 'jpg', 'jpeg', 'eps']
    if format_str.lower() not in valid_formats:
        raise ValueError(f"format must be one of {valid_formats}, got '{format_str}'")

    # Create parent directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    try:
        fig.savefig(
            filepath,
            format=format_str,
            dpi=dpi,
            transparent=transparent,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
        )
        logger.info(f"Saved figure to {filepath} ({format_str}, {dpi} DPI)")
    except Exception as e:
        raise ValueError(f"Failed to save figure to {filepath}: {e}") from e


def save_multiple_formats(
    fig: Figure,
    base_filepath: str | Path,
    formats: list[str],
    dpi: int = 300,
    transparent: bool = False,
) -> list[Path]:
    """
    Save a figure in multiple formats simultaneously.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure to save.
    base_filepath : str | Path
        Base file path without extension.
    formats : list[str]
        List of formats to save ('png', 'svg', 'pdf', etc.).
    dpi : int, optional
        Resolution in dots per inch for raster formats (by default 300).
    transparent : bool, optional
        Whether to use transparent background (by default False).

    Returns
    -------
    list[Path]
        List of created file paths.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If formats list is empty or contains invalid formats.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 2])
    >>> paths = save_multiple_formats(fig, 'output/plot', ['png', 'svg', 'pdf'])
    >>> len(paths)
    3

    Notes
    -----
    Convenient for generating publication-ready figures in multiple formats
    with a single function call.

    Complexity
    ----------
    Time: O(n*m) where n is figure complexity and m is number of formats
    Space: O(1)
    """
    # Type validation
    if not isinstance(fig, Figure):
        raise TypeError(f"fig must be a matplotlib Figure, got {type(fig).__name__}")
    if not isinstance(base_filepath, (str, Path)):
        raise TypeError(f"base_filepath must be a string or Path, got {type(base_filepath).__name__}")
    if not isinstance(formats, list):
        raise TypeError(f"formats must be a list, got {type(formats).__name__}")
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")
    if not isinstance(transparent, bool):
        raise TypeError(f"transparent must be a boolean, got {type(transparent).__name__}")

    # Value validation
    if len(formats) == 0:
        raise ValueError("formats list cannot be empty")
    if not all(isinstance(fmt, str) for fmt in formats):
        raise TypeError("All format items must be strings")
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")

    # Convert to Path and remove extension if present
    base_filepath = Path(base_filepath)
    if base_filepath.suffix:
        base_filepath = base_filepath.with_suffix('')

    # Save in each format
    saved_paths = []
    for fmt in formats:
        filepath = base_filepath.with_suffix(f'.{fmt}')
        save_figure(
            fig,
            filepath,
            format=fmt,
            dpi=dpi,
            transparent=transparent,
        )
        saved_paths.append(filepath)

    logger.info(f"Saved figure in {len(formats)} formats: {', '.join(formats)}")
    return saved_paths


def export_current_figure(
    filepath: str | Path,
    format: Literal['png', 'svg', 'pdf', 'jpg', 'eps'] | None = None,
    dpi: int = 300,
    close_after_save: bool = False,
) -> None:
    """
    Export the current matplotlib figure (gcf).

    Parameters
    ----------
    filepath : str | Path
        Output file path.
    format : Literal['png', 'svg', 'pdf', 'jpg', 'eps'] | None, optional
        Output format. If None, inferred from filepath extension (by default None).
    dpi : int, optional
        Resolution in dots per inch for raster formats (by default 300).
    close_after_save : bool, optional
        Whether to close the figure after saving (by default False).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If no current figure exists or parameters are invalid.

    Examples
    --------
    >>> plt.plot([1, 2, 3], [1, 4, 2])
    >>> plt.title("Sample Plot")
    >>> export_current_figure('plot.png', dpi=300)

    >>> # Save and close
    >>> plt.plot([1, 2, 3], [1, 4, 2])
    >>> export_current_figure('plot.svg', close_after_save=True)

    Notes
    -----
    Convenient shorthand for saving the current active figure without
    explicitly getting the figure object.

    Complexity
    ----------
    Time: O(n) where n is figure complexity, Space: O(1)
    """
    # Type validation
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"filepath must be a string or Path, got {type(filepath).__name__}")
    if format is not None and not isinstance(format, str):
        raise TypeError(f"format must be a string or None, got {type(format).__name__}")
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")
    if not isinstance(close_after_save, bool):
        raise TypeError(f"close_after_save must be a boolean, got {type(close_after_save).__name__}")

    # Value validation
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")

    # Get current figure
    fig = plt.gcf()
    if fig is None:
        raise ValueError("No current figure exists. Create a plot first.")

    # Save figure
    save_figure(fig, filepath, format=format, dpi=dpi)

    # Close if requested
    if close_after_save:
        plt.close(fig)
        logger.debug("Closed figure after saving")


def create_figure_grid(
    figures: list[Figure],
    output_path: str | Path,
    n_cols: int = 2,
    figsize: tuple[int, int] | None = None,
    dpi: int = 300,
) -> None:
    """
    Combine multiple figures into a single grid layout and save.

    Parameters
    ----------
    figures : list[Figure]
        List of matplotlib figures to combine.
    output_path : str | Path
        Output file path for the combined figure.
    n_cols : int, optional
        Number of columns in the grid (by default 2).
    figsize : tuple[int, int] | None, optional
        Size of the combined figure. If None, auto-calculated (by default None).
    dpi : int, optional
        Resolution in dots per inch (by default 300).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If figures list is empty or parameters are invalid.

    Examples
    --------
    >>> fig1, ax1 = plt.subplots()
    >>> ax1.plot([1, 2, 3], [1, 4, 2])
    >>> fig2, ax2 = plt.subplots()
    >>> ax2.plot([1, 2, 3], [2, 3, 1])
    >>> create_figure_grid([fig1, fig2], 'combined.png', n_cols=2)

    Notes
    -----
    Useful for creating multi-panel figures for publications or reports.
    Each input figure becomes a subplot in the combined output.

    Complexity
    ----------
    Time: O(n) where n is number of figures, Space: O(n)
    """
    # Type validation
    if not isinstance(figures, list):
        raise TypeError(f"figures must be a list, got {type(figures).__name__}")
    if not isinstance(output_path, (str, Path)):
        raise TypeError(f"output_path must be a string or Path, got {type(output_path).__name__}")
    if not isinstance(n_cols, int):
        raise TypeError(f"n_cols must be an integer, got {type(n_cols).__name__}")
    if figsize is not None and (not isinstance(figsize, tuple) or len(figsize) != 2):
        raise TypeError("figsize must be a tuple of two integers or None")
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")

    # Value validation
    if len(figures) == 0:
        raise ValueError("figures list cannot be empty")
    if not all(isinstance(fig, Figure) for fig in figures):
        raise TypeError("All items in figures must be matplotlib Figure objects")
    if n_cols <= 0:
        raise ValueError(f"n_cols must be positive, got {n_cols}")
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")

    # Calculate grid dimensions
    n_figs = len(figures)
    n_rows = (n_figs + n_cols - 1) // n_cols  # Ceiling division

    # Auto-calculate figsize if not provided
    if figsize is None:
        single_width = 5
        single_height = 4
        figsize = (n_cols * single_width, n_rows * single_height)

    # Create combined figure
    combined_fig = plt.figure(figsize=figsize)

    for idx, fig in enumerate(figures):
        # Create subplot in grid
        ax = combined_fig.add_subplot(n_rows, n_cols, idx + 1)

        # Copy content from original figure
        # Get all axes from the original figure
        orig_axes = fig.get_axes()
        if len(orig_axes) > 0:
            orig_ax = orig_axes[0]

            # Copy lines
            for line in orig_ax.get_lines():
                ax.plot(line.get_xdata(), line.get_ydata(),
                       color=line.get_color(),
                       linestyle=line.get_linestyle(),
                       marker=line.get_marker(),
                       label=line.get_label())

            # Copy collections (scatter plots, etc.)
            for collection in orig_ax.collections:
                ax.add_collection(collection)

            # Copy labels and title
            ax.set_xlabel(orig_ax.get_xlabel())
            ax.set_ylabel(orig_ax.get_ylabel())
            ax.set_title(orig_ax.get_title())

            # Copy legend if present
            legend = orig_ax.get_legend()
            if legend is not None:
                ax.legend()

    plt.tight_layout()

    # Save combined figure
    save_figure(combined_fig, output_path, dpi=dpi)

    logger.info(f"Created figure grid with {n_figs} figures ({n_rows}x{n_cols})")
    plt.close(combined_fig)


def configure_export_defaults(
    default_dpi: int = 300,
    default_format: str = 'png',
    default_transparent: bool = False,
) -> None:
    """
    Configure default settings for figure exports.

    Parameters
    ----------
    default_dpi : int, optional
        Default DPI for saved figures (by default 300).
    default_format : str, optional
        Default file format (by default 'png').
    default_transparent : bool, optional
        Default transparency setting (by default False).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> configure_export_defaults(dpi=600, format='svg', transparent=True)
    >>> # All subsequent exports use these defaults

    Notes
    -----
    This sets matplotlib's global savefig parameters. These settings affect
    all save operations until changed or reset.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(default_dpi, int):
        raise TypeError(f"default_dpi must be an integer, got {type(default_dpi).__name__}")
    if not isinstance(default_format, str):
        raise TypeError(f"default_format must be a string, got {type(default_format).__name__}")
    if not isinstance(default_transparent, bool):
        raise TypeError(f"default_transparent must be a boolean, got {type(default_transparent).__name__}")

    # Value validation
    if default_dpi <= 0:
        raise ValueError(f"default_dpi must be positive, got {default_dpi}")

    valid_formats = ['png', 'svg', 'pdf', 'jpg', 'jpeg', 'eps']
    if default_format.lower() not in valid_formats:
        raise ValueError(f"default_format must be one of {valid_formats}, got '{default_format}'")

    # Configure matplotlib defaults
    plt.rcParams['savefig.dpi'] = default_dpi
    plt.rcParams['savefig.format'] = default_format
    plt.rcParams['savefig.transparent'] = default_transparent
    plt.rcParams['savefig.bbox'] = 'tight'

    logger.info(f"Configured export defaults: {default_format}, {default_dpi} DPI, transparent={default_transparent}")


__all__ = [
    'save_figure',
    'save_multiple_formats',
    'export_current_figure',
    'create_figure_grid',
    'configure_export_defaults',
]
