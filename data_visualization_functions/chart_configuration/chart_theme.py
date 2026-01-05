"""
Configuration for chart theme and styling.
"""

import logging
from dataclasses import dataclass, field

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


__all__ = ['ChartTheme']
