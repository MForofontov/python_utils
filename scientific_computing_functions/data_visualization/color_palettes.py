"""
Color palette generators and color manipulation utilities.

This module provides functions for generating color palettes, gradients, and
color schemes suitable for data visualization with accessibility considerations.
"""

import logging
from typing import Literal

import matplotlib.colors as mcolors
import numpy as np

logger = logging.getLogger(__name__)


def generate_color_palette(
    n_colors: int,
    palette_type: Literal['sequential', 'diverging', 'qualitative', 'rainbow'] = 'qualitative',
    start_color: str | None = None,
    end_color: str | None = None,
    colormap: str | None = None,
) -> list[str]:
    """
    Generate a color palette with specified number of colors.

    Parameters
    ----------
    n_colors : int
        Number of colors to generate.
    palette_type : Literal['sequential', 'diverging', 'qualitative', 'rainbow'], optional
        Type of color palette (by default 'qualitative').
    start_color : str | None, optional
        Starting color for gradient (hex or named color) (by default None).
    end_color : str | None, optional
        Ending color for gradient (hex or named color) (by default None).
    colormap : str | None, optional
        Matplotlib colormap name to use (by default None).

    Returns
    -------
    list[str]
        List of color hex codes.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> colors = generate_color_palette(5, palette_type='qualitative')
    >>> len(colors)
    5

    >>> colors = generate_color_palette(
    ...     10,
    ...     palette_type='sequential',
    ...     start_color='#FFFFFF',
    ...     end_color='#0000FF'
    ... )
    >>> len(colors)
    10

    >>> colors = generate_color_palette(8, colormap='viridis')
    >>> len(colors)
    8

    Notes
    -----
    Palette types:
    - sequential: Colors transition smoothly from start to end
    - diverging: Colors diverge from center (requires start and end colors)
    - qualitative: Distinct colors for categorical data
    - rainbow: Full spectrum of hues

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is n_colors
    """
    # Type validation
    if not isinstance(n_colors, int):
        raise TypeError(f"n_colors must be an integer, got {type(n_colors).__name__}")
    if not isinstance(palette_type, str):
        raise TypeError(f"palette_type must be a string, got {type(palette_type).__name__}")
    if start_color is not None and not isinstance(start_color, str):
        raise TypeError(f"start_color must be a string or None, got {type(start_color).__name__}")
    if end_color is not None and not isinstance(end_color, str):
        raise TypeError(f"end_color must be a string or None, got {type(end_color).__name__}")
    if colormap is not None and not isinstance(colormap, str):
        raise TypeError(f"colormap must be a string or None, got {type(colormap).__name__}")

    # Value validation
    if n_colors <= 0:
        raise ValueError(f"n_colors must be positive, got {n_colors}")

    valid_palette_types = ['sequential', 'diverging', 'qualitative', 'rainbow']
    if palette_type not in valid_palette_types:
        raise ValueError(f"palette_type must be one of {valid_palette_types}, got '{palette_type}'")

    # Use specified colormap if provided
    if colormap is not None:
        try:
            cmap = plt.get_cmap(colormap)
            colors = [mcolors.rgb2hex(cmap(i / (n_colors - 1 if n_colors > 1 else 1))) 
                     for i in range(n_colors)]
            logger.debug(f"Generated {n_colors} colors from colormap '{colormap}'")
            return colors
        except Exception as e:
            raise ValueError(f"Invalid colormap '{colormap}': {e}") from e

    # Generate colors based on palette type
    if palette_type == 'qualitative':
        # Use distinct colors from tableau palette
        base_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        if n_colors <= len(base_colors):
            colors = base_colors[:n_colors]
        else:
            # Generate additional colors using HSV
            colors = base_colors.copy()
            hues = np.linspace(0, 1, n_colors - len(base_colors) + 1)[:-1]
            for hue in hues:
                rgb = mcolors.hsv_to_rgb([hue, 0.7, 0.9])
                colors.append(mcolors.rgb2hex(rgb))

    elif palette_type == 'sequential':
        # Sequential gradient
        if start_color is None:
            start_color = '#FFFFFF'
        if end_color is None:
            end_color = '#0000FF'

        start_rgb = mcolors.to_rgb(start_color)
        end_rgb = mcolors.to_rgb(end_color)

        colors = []
        for i in range(n_colors):
            t = i / (n_colors - 1) if n_colors > 1 else 0
            rgb = [start_rgb[j] + t * (end_rgb[j] - start_rgb[j]) for j in range(3)]
            colors.append(mcolors.rgb2hex(rgb))

    elif palette_type == 'diverging':
        # Diverging from center
        if start_color is None:
            start_color = '#0000FF'
        if end_color is None:
            end_color = '#FF0000'

        mid_color = '#FFFFFF'
        start_rgb = mcolors.to_rgb(start_color)
        mid_rgb = mcolors.to_rgb(mid_color)
        end_rgb = mcolors.to_rgb(end_color)

        colors = []
        for i in range(n_colors):
            t = i / (n_colors - 1) if n_colors > 1 else 0
            if t < 0.5:
                # Interpolate from start to mid
                t_scaled = t * 2
                rgb = [start_rgb[j] + t_scaled * (mid_rgb[j] - start_rgb[j]) for j in range(3)]
            else:
                # Interpolate from mid to end
                t_scaled = (t - 0.5) * 2
                rgb = [mid_rgb[j] + t_scaled * (end_rgb[j] - mid_rgb[j]) for j in range(3)]
            colors.append(mcolors.rgb2hex(rgb))

    else:  # rainbow
        # Full spectrum
        hues = np.linspace(0, 1, n_colors + 1)[:-1]
        colors = []
        for hue in hues:
            rgb = mcolors.hsv_to_rgb([hue, 0.8, 0.9])
            colors.append(mcolors.rgb2hex(rgb))

    logger.debug(f"Generated {n_colors} colors with palette_type='{palette_type}'")
    return colors


def create_gradient(
    start_color: str,
    end_color: str,
    n_steps: int = 10,
) -> list[str]:
    """
    Create a smooth color gradient between two colors.

    Parameters
    ----------
    start_color : str
        Starting color (hex code or named color).
    end_color : str
        Ending color (hex code or named color).
    n_steps : int, optional
        Number of steps in the gradient (by default 10).

    Returns
    -------
    list[str]
        List of color hex codes forming the gradient.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> gradient = create_gradient('#FF0000', '#0000FF', n_steps=5)
    >>> len(gradient)
    5

    >>> gradient = create_gradient('red', 'blue', n_steps=10)
    >>> len(gradient)
    10

    Notes
    -----
    The gradient is created by linear interpolation in RGB space.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is n_steps
    """
    # Type validation
    if not isinstance(start_color, str):
        raise TypeError(f"start_color must be a string, got {type(start_color).__name__}")
    if not isinstance(end_color, str):
        raise TypeError(f"end_color must be a string, got {type(end_color).__name__}")
    if not isinstance(n_steps, int):
        raise TypeError(f"n_steps must be an integer, got {type(n_steps).__name__}")

    # Value validation
    if n_steps <= 0:
        raise ValueError(f"n_steps must be positive, got {n_steps}")

    try:
        start_rgb = mcolors.to_rgb(start_color)
        end_rgb = mcolors.to_rgb(end_color)
    except ValueError as e:
        raise ValueError(f"Invalid color specification: {e}") from e

    gradient = []
    for i in range(n_steps):
        t = i / (n_steps - 1) if n_steps > 1 else 0
        rgb = [start_rgb[j] + t * (end_rgb[j] - start_rgb[j]) for j in range(3)]
        gradient.append(mcolors.rgb2hex(rgb))

    logger.debug(f"Created gradient with {n_steps} steps from {start_color} to {end_color}")
    return gradient


def get_colorblind_safe_palette(n_colors: int) -> list[str]:
    """
    Generate a colorblind-safe color palette.

    Parameters
    ----------
    n_colors : int
        Number of colors needed.

    Returns
    -------
    list[str]
        List of colorblind-safe hex color codes.

    Raises
    ------
    TypeError
        If n_colors is not an integer.
    ValueError
        If n_colors is not positive or exceeds maximum available colors.

    Examples
    --------
    >>> colors = get_colorblind_safe_palette(5)
    >>> len(colors)
    5

    >>> colors = get_colorblind_safe_palette(8)
    >>> # All colors are distinguishable for colorblind viewers

    Notes
    -----
    Uses Paul Tol's colorblind-safe color schemes. Maximum 12 colors available.
    For more colors, consider using different markers or line styles.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(n_colors, int):
        raise TypeError(f"n_colors must be an integer, got {type(n_colors).__name__}")

    # Value validation
    if n_colors <= 0:
        raise ValueError(f"n_colors must be positive, got {n_colors}")

    # Paul Tol's colorblind-safe palette
    colorblind_safe = [
        '#4477AA',  # Blue
        '#EE6677',  # Red
        '#228833',  # Green
        '#CCBB44',  # Yellow
        '#66CCEE',  # Cyan
        '#AA3377',  # Purple
        '#BBBBBB',  # Grey
        '#EE7733',  # Orange
        '#009988',  # Teal
        '#CC3311',  # Dark red
        '#33BBEE',  # Light blue
        '#EE3377',  # Magenta
    ]

    if n_colors > len(colorblind_safe):
        raise ValueError(
            f"n_colors ({n_colors}) exceeds maximum colorblind-safe colors ({len(colorblind_safe)}). "
            "Consider using different markers or line styles for additional distinction."
        )

    colors = colorblind_safe[:n_colors]
    logger.debug(f"Retrieved {n_colors} colorblind-safe colors")
    return colors


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convert hex color code to RGB tuple.

    Parameters
    ----------
    hex_color : str
        Hex color code (e.g., '#FF0000' or 'FF0000').

    Returns
    -------
    tuple[int, int, int]
        RGB values as integers (0-255).

    Raises
    ------
    TypeError
        If hex_color is not a string.
    ValueError
        If hex_color is not a valid hex code.

    Examples
    --------
    >>> hex_to_rgb('#FF0000')
    (255, 0, 0)

    >>> hex_to_rgb('00FF00')
    (0, 255, 0)

    Notes
    -----
    Accepts hex codes with or without the leading '#' symbol.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(hex_color, str):
        raise TypeError(f"hex_color must be a string, got {type(hex_color).__name__}")

    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Value validation
    if len(hex_color) != 6:
        raise ValueError(f"hex_color must be 6 characters (excluding #), got '{hex_color}'")

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError as e:
        raise ValueError(f"Invalid hex color code '{hex_color}': {e}") from e

    logger.debug(f"Converted {hex_color} to RGB({r}, {g}, {b})")
    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hex color code.

    Parameters
    ----------
    r : int
        Red value (0-255).
    g : int
        Green value (0-255).
    b : int
        Blue value (0-255).

    Returns
    -------
    str
        Hex color code with leading '#'.

    Raises
    ------
    TypeError
        If parameters are not integers.
    ValueError
        If values are not in range 0-255.

    Examples
    --------
    >>> rgb_to_hex(255, 0, 0)
    '#FF0000'

    >>> rgb_to_hex(0, 255, 0)
    '#00FF00'

    Notes
    -----
    All RGB values must be in the range [0, 255].

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(r, int):
        raise TypeError(f"r must be an integer, got {type(r).__name__}")
    if not isinstance(g, int):
        raise TypeError(f"g must be an integer, got {type(g).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    # Value validation
    if not 0 <= r <= 255:
        raise ValueError(f"r must be in range [0, 255], got {r}")
    if not 0 <= g <= 255:
        raise ValueError(f"g must be in range [0, 255], got {g}")
    if not 0 <= b <= 255:
        raise ValueError(f"b must be in range [0, 255], got {b}")

    hex_code = f"#{r:02X}{g:02X}{b:02X}"
    logger.debug(f"Converted RGB({r}, {g}, {b}) to {hex_code}")
    return hex_code


def adjust_brightness(
    color: str,
    factor: float,
) -> str:
    """
    Adjust the brightness of a color.

    Parameters
    ----------
    color : str
        Input color (hex code or named color).
    factor : float
        Brightness adjustment factor. Values > 1.0 brighten, < 1.0 darken.

    Returns
    -------
    str
        Adjusted color as hex code.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If factor is not positive or color is invalid.

    Examples
    --------
    >>> adjust_brightness('#0000FF', 1.5)  # Brighter blue
    '#0000FF'  # (will be lighter)

    >>> adjust_brightness('#FF0000', 0.5)  # Darker red
    '#800000'

    Notes
    -----
    Brightness adjustment is done by scaling RGB values. Values are clamped
    to the valid range [0, 255].

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(color, str):
        raise TypeError(f"color must be a string, got {type(color).__name__}")
    if not isinstance(factor, (int, float)):
        raise TypeError(f"factor must be a number, got {type(factor).__name__}")

    # Value validation
    if factor <= 0:
        raise ValueError(f"factor must be positive, got {factor}")

    try:
        rgb = mcolors.to_rgb(color)
    except ValueError as e:
        raise ValueError(f"Invalid color specification '{color}': {e}") from e

    # Adjust brightness by scaling RGB values
    adjusted_rgb = [min(1.0, max(0.0, channel * factor)) for channel in rgb]
    adjusted_hex = mcolors.rgb2hex(adjusted_rgb)

    logger.debug(f"Adjusted brightness of {color} by factor {factor} to {adjusted_hex}")
    return adjusted_hex


def generate_categorical_colors(categories: list[str]) -> dict[str, str]:
    """
    Generate a mapping of categories to distinct colors.

    Parameters
    ----------
    categories : list[str]
        List of category names.

    Returns
    -------
    dict[str, str]
        Dictionary mapping category names to hex color codes.

    Raises
    ------
    TypeError
        If categories is not a list.
    ValueError
        If categories is empty or contains non-string values.

    Examples
    --------
    >>> categories = ['A', 'B', 'C']
    >>> color_map = generate_categorical_colors(categories)
    >>> len(color_map)
    3
    >>> 'A' in color_map
    True

    Notes
    -----
    Uses colorblind-safe palette when possible, falls back to qualitative
    palette for larger category sets.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is number of categories
    """
    # Type validation
    if not isinstance(categories, list):
        raise TypeError(f"categories must be a list, got {type(categories).__name__}")

    # Value validation
    if len(categories) == 0:
        raise ValueError("categories cannot be empty")

    if not all(isinstance(cat, str) for cat in categories):
        raise TypeError("All category items must be strings")

    # Check for duplicates
    if len(categories) != len(set(categories)):
        logger.warning("Duplicate categories found, using first occurrence")
        categories = list(dict.fromkeys(categories))  # Preserve order, remove duplicates

    # Use colorblind-safe palette if possible
    n_colors = len(categories)
    try:
        colors = get_colorblind_safe_palette(n_colors)
    except ValueError:
        # Fall back to qualitative palette for large category sets
        colors = generate_color_palette(n_colors, palette_type='qualitative')

    color_map = dict(zip(categories, colors))
    logger.debug(f"Generated color mapping for {n_colors} categories")
    return color_map


# Import matplotlib.pyplot for colormap access
import matplotlib.pyplot as plt  # noqa: E402


__all__ = [
    'generate_color_palette',
    'create_gradient',
    'get_colorblind_safe_palette',
    'hex_to_rgb',
    'rgb_to_hex',
    'adjust_brightness',
    'generate_categorical_colors',
]
