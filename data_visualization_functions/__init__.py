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
from .plot_generation import (
    create_line_plot,
    create_scatter_plot,
    create_bar_plot,
    create_histogram,
)

# Chart configuration utilities
from .chart_configuration import (
    ChartTheme,
    get_preset_theme,
    apply_theme,
    reset_theme,
    configure_axes_style,
    set_figure_size,
)

# Color palette generators
from .color_palettes import (
    generate_color_palette,
    create_gradient,
    get_colorblind_safe_palette,
    hex_to_rgb,
    rgb_to_hex,
    adjust_brightness,
    generate_categorical_colors,
)

# Data-to-visualization transformers
from .data_transformers import (
    normalize_data,
    bin_data,
    aggregate_by_group,
    pivot_for_heatmap,
    smooth_timeseries,
    calculate_moving_statistics,
)

# Export utilities
from .export_utilities import (
    save_figure,
    save_multiple_formats,
    export_current_figure,
    create_figure_grid,
    configure_export_defaults,
)

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
