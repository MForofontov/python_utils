"""
Data Visualization Functions

This module provides comprehensive utilities for data visualization including:
- Plot generation helpers (matplotlib/plotly wrappers)
- Chart configuration utilities
- Color palette generators
- Data-to-visualization transformers
- Export utilities (SVG, PNG, PDF)
"""

# Plot generation helpers
from .create_line_plot import create_line_plot
from .create_scatter_plot import create_scatter_plot
from .create_bar_plot import create_bar_plot
from .create_histogram import create_histogram

# Chart configuration utilities
from .chart_theme import ChartTheme
from .get_preset_theme import get_preset_theme
from .apply_theme import apply_theme
from .reset_theme import reset_theme
from .configure_axes_style import configure_axes_style
from .set_figure_size import set_figure_size

# Color palette generators
from .generate_color_palette import generate_color_palette
from .create_gradient import create_gradient
from .get_colorblind_safe_palette import get_colorblind_safe_palette
from .hex_to_rgb import hex_to_rgb
from .rgb_to_hex import rgb_to_hex
from .adjust_brightness import adjust_brightness
from .generate_categorical_colors import generate_categorical_colors

# Data-to-visualization transformers
from .normalize_data import normalize_data
from .bin_data import bin_data
from .aggregate_by_group import aggregate_by_group
from .pivot_for_heatmap import pivot_for_heatmap
from .smooth_timeseries import smooth_timeseries
from .calculate_moving_statistics import calculate_moving_statistics

# Export utilities
from .save_figure import save_figure
from .save_multiple_formats import save_multiple_formats
from .export_current_figure import export_current_figure
from .create_figure_grid import create_figure_grid
from .configure_export_defaults import configure_export_defaults

__all__ = [
    # Plot generation helpers
    'create_line_plot',
    'create_scatter_plot',
    'create_bar_plot',
    'create_histogram',
    # Chart configuration utilities
    'ChartTheme',
    'get_preset_theme',
    'apply_theme',
    'reset_theme',
    'configure_axes_style',
    'set_figure_size',
    # Color palette generators
    'generate_color_palette',
    'create_gradient',
    'get_colorblind_safe_palette',
    'hex_to_rgb',
    'rgb_to_hex',
    'adjust_brightness',
    'generate_categorical_colors',
    # Data-to-visualization transformers
    'normalize_data',
    'bin_data',
    'aggregate_by_group',
    'pivot_for_heatmap',
    'smooth_timeseries',
    'calculate_moving_statistics',
    # Export utilities
    'save_figure',
    'save_multiple_formats',
    'export_current_figure',
    'create_figure_grid',
    'configure_export_defaults',
]

# Version - import from central _version.py
from .._version import __version__
