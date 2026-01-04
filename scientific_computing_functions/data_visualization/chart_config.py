"""
Chart configuration utilities for consistent styling and theming.

This module provides utilities for creating and managing chart configurations,
themes, and styling options to ensure consistent visualization across projects.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

import matplotlib.pyplot as plt
from matplotlib import cycler

logger = logging.getLogger(__name__)


@dataclass
class ChartTheme:
    """
    Configuration for chart theme and styling.

    Attributes
    ----------
    name : str
        Theme name.
    background_color : str
        Background color for plots.
    grid_color : str
        Grid line color.
    grid_alpha : float
        Grid transparency.
    title_fontsize : int
        Font size for titles.
    label_fontsize : int
        Font size for axis labels.
    tick_fontsize : int
        Font size for tick labels.
    legend_fontsize : int
        Font size for legend.
    line_width : float
        Default line width.
    color_cycle : list[str]
        Color cycle for multiple series.
    font_family : str
        Font family to use.

    Examples
    --------
    >>> theme = ChartTheme(
    ...     name="corporate",
    ...     background_color="white",
    ...     color_cycle=["#1f77b4", "#ff7f0e", "#2ca02c"]
    ... )
    >>> apply_theme(theme)
    """

    name: str
    background_color: str = "white"
    grid_color: str = "#cccccc"
    grid_alpha: float = 0.3
    title_fontsize: int = 14
    label_fontsize: int = 12
    tick_fontsize: int = 10
    legend_fontsize: int = 10
    line_width: float = 2.0
    color_cycle: list[str] = field(default_factory=lambda: [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ])
    font_family: str = "sans-serif"

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not isinstance(self.name, str):
            raise TypeError(f"name must be a string, got {type(self.name).__name__}")
        if not isinstance(self.background_color, str):
            raise TypeError(f"background_color must be a string, got {type(self.background_color).__name__}")
        if not isinstance(self.grid_color, str):
            raise TypeError(f"grid_color must be a string, got {type(self.grid_color).__name__}")
        if not isinstance(self.grid_alpha, (int, float)):
            raise TypeError(f"grid_alpha must be a number, got {type(self.grid_alpha).__name__}")
        if not 0 <= self.grid_alpha <= 1:
            raise ValueError(f"grid_alpha must be between 0 and 1, got {self.grid_alpha}")
        if not isinstance(self.title_fontsize, int):
            raise TypeError(f"title_fontsize must be an integer, got {type(self.title_fontsize).__name__}")
        if self.title_fontsize <= 0:
            raise ValueError(f"title_fontsize must be positive, got {self.title_fontsize}")
        if not isinstance(self.label_fontsize, int):
            raise TypeError(f"label_fontsize must be an integer, got {type(self.label_fontsize).__name__}")
        if self.label_fontsize <= 0:
            raise ValueError(f"label_fontsize must be positive, got {self.label_fontsize}")
        if not isinstance(self.tick_fontsize, int):
            raise TypeError(f"tick_fontsize must be an integer, got {type(self.tick_fontsize).__name__}")
        if self.tick_fontsize <= 0:
            raise ValueError(f"tick_fontsize must be positive, got {self.tick_fontsize}")
        if not isinstance(self.legend_fontsize, int):
            raise TypeError(f"legend_fontsize must be an integer, got {type(self.legend_fontsize).__name__}")
        if self.legend_fontsize <= 0:
            raise ValueError(f"legend_fontsize must be positive, got {self.legend_fontsize}")
        if not isinstance(self.line_width, (int, float)):
            raise TypeError(f"line_width must be a number, got {type(self.line_width).__name__}")
        if self.line_width <= 0:
            raise ValueError(f"line_width must be positive, got {self.line_width}")
        if not isinstance(self.color_cycle, list):
            raise TypeError(f"color_cycle must be a list, got {type(self.color_cycle).__name__}")
        if len(self.color_cycle) == 0:
            raise ValueError("color_cycle cannot be empty")
        if not isinstance(self.font_family, str):
            raise TypeError(f"font_family must be a string, got {type(self.font_family).__name__}")


def get_preset_theme(
    theme_name: Literal['default', 'dark', 'minimal', 'colorful', 'presentation', 'publication']
) -> ChartTheme:
    """
    Get a preset theme configuration.

    Parameters
    ----------
    theme_name : Literal['default', 'dark', 'minimal', 'colorful', 'presentation', 'publication']
        Name of the preset theme.

    Returns
    -------
    ChartTheme
        Configured theme object.

    Raises
    ------
    TypeError
        If theme_name is not a string.
    ValueError
        If theme_name is not a valid preset.

    Examples
    --------
    >>> theme = get_preset_theme('dark')
    >>> apply_theme(theme)

    >>> theme = get_preset_theme('presentation')
    >>> # Use for slides with high contrast and large fonts

    Notes
    -----
    Available themes:
    - default: Standard matplotlib colors
    - dark: Dark background with light colors
    - minimal: Clean, minimal styling
    - colorful: Vibrant colors
    - presentation: Large fonts for presentations
    - publication: Print-friendly grayscale-compatible

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(theme_name, str):
        raise TypeError(f"theme_name must be a string, got {type(theme_name).__name__}")

    valid_themes = ['default', 'dark', 'minimal', 'colorful', 'presentation', 'publication']
    if theme_name not in valid_themes:
        raise ValueError(f"theme_name must be one of {valid_themes}, got '{theme_name}'")

    themes: dict[str, ChartTheme] = {
        'default': ChartTheme(
            name='default',
            background_color='white',
            grid_color='#cccccc',
            grid_alpha=0.3,
        ),
        'dark': ChartTheme(
            name='dark',
            background_color='#1a1a1a',
            grid_color='#444444',
            grid_alpha=0.5,
            color_cycle=[
                "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3",
                "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd"
            ],
        ),
        'minimal': ChartTheme(
            name='minimal',
            background_color='white',
            grid_color='#e0e0e0',
            grid_alpha=0.2,
            line_width=1.5,
            color_cycle=["#333333", "#666666", "#999999", "#cccccc"],
        ),
        'colorful': ChartTheme(
            name='colorful',
            background_color='white',
            grid_color='#eeeeee',
            grid_alpha=0.4,
            color_cycle=[
                "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
                "#1abc9c", "#e67e22", "#34495e", "#95a5a6", "#c0392b"
            ],
        ),
        'presentation': ChartTheme(
            name='presentation',
            background_color='white',
            grid_color='#dddddd',
            grid_alpha=0.4,
            title_fontsize=18,
            label_fontsize=14,
            tick_fontsize=12,
            legend_fontsize=12,
            line_width=3.0,
        ),
        'publication': ChartTheme(
            name='publication',
            background_color='white',
            grid_color='#cccccc',
            grid_alpha=0.3,
            title_fontsize=11,
            label_fontsize=10,
            tick_fontsize=9,
            legend_fontsize=9,
            line_width=1.5,
            color_cycle=[
                "#000000", "#555555", "#888888", "#aaaaaa", "#333333",
                "#666666", "#999999", "#bbbbbb", "#222222", "#777777"
            ],
            font_family='serif',
        ),
    }

    theme = themes[theme_name]
    logger.debug(f"Retrieved preset theme: {theme_name}")
    return theme


def apply_theme(theme: ChartTheme) -> None:
    """
    Apply a theme to matplotlib's global configuration.

    Parameters
    ----------
    theme : ChartTheme
        Theme configuration to apply.

    Raises
    ------
    TypeError
        If theme is not a ChartTheme instance.

    Examples
    --------
    >>> theme = get_preset_theme('dark')
    >>> apply_theme(theme)
    >>> # All subsequent plots will use the dark theme

    >>> custom_theme = ChartTheme(
    ...     name="custom",
    ...     background_color="#f5f5f5",
    ...     color_cycle=["#FF6B6B", "#4ECDC4", "#45B7D1"]
    ... )
    >>> apply_theme(custom_theme)

    Notes
    -----
    This function modifies matplotlib's global rcParams. Changes persist
    for the entire session unless reset with reset_theme().

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(theme, ChartTheme):
        raise TypeError(f"theme must be a ChartTheme instance, got {type(theme).__name__}")

    # Apply theme settings
    plt.rcParams['figure.facecolor'] = theme.background_color
    plt.rcParams['axes.facecolor'] = theme.background_color
    plt.rcParams['axes.edgecolor'] = theme.grid_color
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = theme.grid_color
    plt.rcParams['grid.alpha'] = theme.grid_alpha
    plt.rcParams['axes.titlesize'] = theme.title_fontsize
    plt.rcParams['axes.labelsize'] = theme.label_fontsize
    plt.rcParams['xtick.labelsize'] = theme.tick_fontsize
    plt.rcParams['ytick.labelsize'] = theme.tick_fontsize
    plt.rcParams['legend.fontsize'] = theme.legend_fontsize
    plt.rcParams['lines.linewidth'] = theme.line_width
    plt.rcParams['font.family'] = theme.font_family

    # Set color cycle
    plt.rcParams['axes.prop_cycle'] = cycler(color=theme.color_cycle)

    logger.info(f"Applied theme: {theme.name}")


def reset_theme() -> None:
    """
    Reset matplotlib configuration to default settings.

    Examples
    --------
    >>> apply_theme(get_preset_theme('dark'))
    >>> # Create some plots...
    >>> reset_theme()
    >>> # Back to default matplotlib settings

    Notes
    -----
    This resets all matplotlib rcParams to their default values.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    plt.rcdefaults()
    logger.info("Reset theme to matplotlib defaults")


def configure_axes_style(
    ax: Any,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    title_fontsize: int | None = None,
    label_fontsize: int | None = None,
    grid: bool = True,
    grid_style: str = '--',
    grid_alpha: float = 0.3,
    spine_visibility: dict[str, bool] | None = None,
) -> None:
    """
    Configure axes styling with comprehensive options.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure.
    title : str, optional
        Title for the axes (by default "").
    xlabel : str, optional
        Label for x-axis (by default "").
    ylabel : str, optional
        Label for y-axis (by default "").
    title_fontsize : int | None, optional
        Font size for title (by default None, uses current setting).
    label_fontsize : int | None, optional
        Font size for labels (by default None, uses current setting).
    grid : bool, optional
        Whether to show grid (by default True).
    grid_style : str, optional
        Grid line style (by default '--').
    grid_alpha : float, optional
        Grid transparency (by default 0.3).
    spine_visibility : dict[str, bool] | None, optional
        Dictionary controlling spine visibility, e.g., {'top': False, 'right': False}
        (by default None).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 2])
    >>> configure_axes_style(
    ...     ax,
    ...     title="Sample Plot",
    ...     xlabel="X Axis",
    ...     ylabel="Y Axis",
    ...     spine_visibility={'top': False, 'right': False}
    ... )

    Notes
    -----
    This function provides fine-grained control over axes appearance,
    commonly used for publication-quality figures.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")
    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")
    if title_fontsize is not None and not isinstance(title_fontsize, int):
        raise TypeError(f"title_fontsize must be an integer or None, got {type(title_fontsize).__name__}")
    if label_fontsize is not None and not isinstance(label_fontsize, int):
        raise TypeError(f"label_fontsize must be an integer or None, got {type(label_fontsize).__name__}")
    if not isinstance(grid, bool):
        raise TypeError(f"grid must be a boolean, got {type(grid).__name__}")
    if not isinstance(grid_style, str):
        raise TypeError(f"grid_style must be a string, got {type(grid_style).__name__}")
    if not isinstance(grid_alpha, (int, float)):
        raise TypeError(f"grid_alpha must be a number, got {type(grid_alpha).__name__}")
    if spine_visibility is not None and not isinstance(spine_visibility, dict):
        raise TypeError(f"spine_visibility must be a dict or None, got {type(spine_visibility).__name__}")

    # Value validation
    if title_fontsize is not None and title_fontsize <= 0:
        raise ValueError(f"title_fontsize must be positive, got {title_fontsize}")
    if label_fontsize is not None and label_fontsize <= 0:
        raise ValueError(f"label_fontsize must be positive, got {label_fontsize}")
    if not 0 <= grid_alpha <= 1:
        raise ValueError(f"grid_alpha must be between 0 and 1, got {grid_alpha}")

    # Apply title and labels
    if title:
        kwargs = {'fontweight': 'bold'}
        if title_fontsize is not None:
            kwargs['fontsize'] = title_fontsize
        ax.set_title(title, **kwargs)

    if xlabel:
        kwargs = {}
        if label_fontsize is not None:
            kwargs['fontsize'] = label_fontsize
        ax.set_xlabel(xlabel, **kwargs)

    if ylabel:
        kwargs = {}
        if label_fontsize is not None:
            kwargs['fontsize'] = label_fontsize
        ax.set_ylabel(ylabel, **kwargs)

    # Configure grid
    if grid:
        ax.grid(True, linestyle=grid_style, alpha=grid_alpha)
    else:
        ax.grid(False)

    # Configure spines
    if spine_visibility is not None:
        for spine_name, visible in spine_visibility.items():
            if spine_name not in ['top', 'bottom', 'left', 'right']:
                raise ValueError(f"Invalid spine name: {spine_name}")
            ax.spines[spine_name].set_visible(visible)

    logger.debug(f"Configured axes style with title='{title}'")


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

    plt.rcParams['figure.figsize'] = (width, height)
    plt.rcParams['figure.dpi'] = dpi

    logger.info(f"Set default figure size to {width}x{height} inches at {dpi} DPI")


__all__ = [
    'ChartTheme',
    'get_preset_theme',
    'apply_theme',
    'reset_theme',
    'configure_axes_style',
    'set_figure_size',
]
