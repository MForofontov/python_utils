"""
Data visualization utilities for creating and exporting plots.

This module provides comprehensive utilities for data visualization including
plot generation, chart configuration, color palette management, data transformation,
and export functionality.
"""

from .chart_config import (
    ChartTheme,
    apply_theme,
    configure_axes_style,
    get_preset_theme,
    reset_theme,
    set_figure_size,
)
from .color_palettes import (
    adjust_brightness,
    create_gradient,
    generate_categorical_colors,
    generate_color_palette,
    get_colorblind_safe_palette,
    hex_to_rgb,
    rgb_to_hex,
)
from .data_transformers import (
    aggregate_by_group,
    bin_data,
    calculate_moving_statistics,
    normalize_data,
    pivot_for_heatmap,
    smooth_timeseries,
)
from .export_utils import (
    configure_export_defaults,
    create_figure_grid,
    export_current_figure,
    save_figure,
    save_multiple_formats,
)
from .plot_helpers import (
    create_bar_plot,
    create_histogram,
    create_line_plot,
    create_scatter_plot,
)

__all__ = [
    # Plot helpers
    'create_line_plot',
    'create_scatter_plot',
    'create_bar_plot',
    'create_histogram',
    # Chart configuration
    'ChartTheme',
    'get_preset_theme',
    'apply_theme',
    'reset_theme',
    'configure_axes_style',
    'set_figure_size',
    # Color palettes
    'generate_color_palette',
    'create_gradient',
    'get_colorblind_safe_palette',
    'hex_to_rgb',
    'rgb_to_hex',
    'adjust_brightness',
    'generate_categorical_colors',
    # Data transformers
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

# Version - import from parent modules
from ..._version import __version__
