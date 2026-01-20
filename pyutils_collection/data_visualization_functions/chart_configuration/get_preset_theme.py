"""
Get a preset theme configuration.
"""

import logging
from typing import Literal

from .chart_theme import ChartTheme

logger = logging.getLogger(__name__)


def get_preset_theme(
    theme_name: Literal[
        "default", "dark", "minimal", "colorful", "presentation", "publication"
    ],
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

    valid_themes = [
        "default",
        "dark",
        "minimal",
        "colorful",
        "presentation",
        "publication",
    ]
    if theme_name not in valid_themes:
        raise ValueError(
            f"theme_name must be one of {valid_themes}, got '{theme_name}'"
        )

    themes: dict[str, ChartTheme] = {
        "default": ChartTheme(
            name="default",
            background_color="white",
            grid_color="#cccccc",
            grid_alpha=0.3,
        ),
        "dark": ChartTheme(
            name="dark",
            background_color="#1a1a1a",
            grid_color="#444444",
            grid_alpha=0.5,
            color_cycle=[
                "#8dd3c7",
                "#ffffb3",
                "#bebada",
                "#fb8072",
                "#80b1d3",
                "#fdb462",
                "#b3de69",
                "#fccde5",
                "#d9d9d9",
                "#bc80bd",
            ],
        ),
        "minimal": ChartTheme(
            name="minimal",
            background_color="white",
            grid_color="#e0e0e0",
            grid_alpha=0.2,
            line_width=1.5,
            color_cycle=["#333333", "#666666", "#999999", "#cccccc"],
        ),
        "colorful": ChartTheme(
            name="colorful",
            background_color="white",
            grid_color="#eeeeee",
            grid_alpha=0.4,
            color_cycle=[
                "#e74c3c",
                "#3498db",
                "#2ecc71",
                "#f39c12",
                "#9b59b6",
                "#1abc9c",
                "#e67e22",
                "#34495e",
                "#95a5a6",
                "#c0392b",
            ],
        ),
        "presentation": ChartTheme(
            name="presentation",
            background_color="white",
            grid_color="#dddddd",
            grid_alpha=0.4,
            title_fontsize=18,
            label_fontsize=14,
            tick_fontsize=12,
            legend_fontsize=12,
            line_width=3.0,
        ),
        "publication": ChartTheme(
            name="publication",
            background_color="white",
            grid_color="#cccccc",
            grid_alpha=0.3,
            title_fontsize=11,
            label_fontsize=10,
            tick_fontsize=9,
            legend_fontsize=9,
            line_width=1.5,
            color_cycle=[
                "#000000",
                "#555555",
                "#888888",
                "#aaaaaa",
                "#333333",
                "#666666",
                "#999999",
                "#bbbbbb",
                "#222222",
                "#777777",
            ],
            font_family="serif",
        ),
    }

    theme = themes[theme_name]
    logger.debug(f"Retrieved preset theme: {theme_name}")
    return theme


__all__ = ["get_preset_theme"]
