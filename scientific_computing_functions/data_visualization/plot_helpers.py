"""
Plot generation helpers using matplotlib and plotly.

This module provides convenient wrapper functions for creating common plot types
with sensible defaults and additional validation and customization options.
"""

import logging
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def create_line_plot(
    x_data: list[float] | np.ndarray,
    y_data: list[float] | np.ndarray | list[list[float]] | list[np.ndarray],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    labels: list[str] | None = None,
    colors: list[str] | None = None,
    line_styles: list[str] | None = None,
    markers: list[str] | None = None,
    grid: bool = True,
    legend: bool = True,
    figsize: tuple[int, int] = (10, 6),
) -> tuple[Figure, Axes]:
    """
    Create a line plot with multiple series and comprehensive customization.

    Parameters
    ----------
    x_data : list[float] | np.ndarray
        X-axis data points.
    y_data : list[float] | np.ndarray | list[list[float]] | list[np.ndarray]
        Y-axis data points. Can be a single series or multiple series.
    title : str, optional
        Plot title (by default "").
    xlabel : str, optional
        X-axis label (by default "").
    ylabel : str, optional
        Y-axis label (by default "").
    labels : list[str] | None, optional
        Legend labels for each series (by default None).
    colors : list[str] | None, optional
        Colors for each series (by default None).
    line_styles : list[str] | None, optional
        Line styles for each series, e.g., '-', '--', '-.', ':' (by default None).
    markers : list[str] | None, optional
        Markers for each series, e.g., 'o', 's', '^' (by default None).
    grid : bool, optional
        Whether to show grid (by default True).
    legend : bool, optional
        Whether to show legend (by default True).
    figsize : tuple[int, int], optional
        Figure size as (width, height) in inches (by default (10, 6)).

    Returns
    -------
    tuple[Figure, Axes]
        Matplotlib figure and axes objects for further customization.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data dimensions don't match or are invalid.

    Examples
    --------
    >>> x = [1, 2, 3, 4, 5]
    >>> y1 = [1, 4, 2, 3, 5]
    >>> y2 = [2, 3, 4, 5, 6]
    >>> fig, ax = create_line_plot(
    ...     x, [y1, y2],
    ...     title="Sales Data",
    ...     xlabel="Month",
    ...     ylabel="Revenue ($)",
    ...     labels=["Product A", "Product B"]
    ... )
    >>> plt.show()

    Notes
    -----
    This function provides a convenient wrapper around matplotlib with sensible
    defaults and automatic handling of multiple series.

    Complexity
    ----------
    Time: O(n*m) where n is data points and m is number of series
    Space: O(n*m)
    """
    # Type validation
    if not isinstance(x_data, (list, np.ndarray)):
        raise TypeError(f"x_data must be a list or numpy array, got {type(x_data).__name__}")
    if not isinstance(y_data, (list, np.ndarray)):
        raise TypeError(f"y_data must be a list or numpy array, got {type(y_data).__name__}")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")
    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")
    if not isinstance(grid, bool):
        raise TypeError(f"grid must be a boolean, got {type(grid).__name__}")
    if not isinstance(legend, bool):
        raise TypeError(f"legend must be a boolean, got {type(legend).__name__}")
    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError("figsize must be a tuple of two integers")

    # Convert to numpy arrays
    x_data = np.asarray(x_data)
    
    # Value validation
    if len(x_data) == 0:
        raise ValueError("x_data cannot be empty")
    
    if figsize[0] <= 0 or figsize[1] <= 0:
        raise ValueError(f"figsize dimensions must be positive, got {figsize}")

    # Handle multiple series
    if isinstance(y_data, np.ndarray) and y_data.ndim == 1:
        y_series = [y_data]
    elif isinstance(y_data, list) and len(y_data) > 0:
        if isinstance(y_data[0], (list, np.ndarray)):
            y_series = [np.asarray(y) for y in y_data]
        else:
            y_series = [np.asarray(y_data)]
    else:
        y_series = [np.asarray(y_data)]

    # Validate dimensions
    for i, y in enumerate(y_series):
        if len(y) != len(x_data):
            raise ValueError(
                f"y_data series {i} length ({len(y)}) must match x_data length ({len(x_data)})"
            )

    num_series = len(y_series)

    # Validate optional parameters
    if labels is not None:
        if not isinstance(labels, list):
            raise TypeError(f"labels must be a list, got {type(labels).__name__}")
        if len(labels) != num_series:
            raise ValueError(f"Number of labels ({len(labels)}) must match number of series ({num_series})")
    
    if colors is not None:
        if not isinstance(colors, list):
            raise TypeError(f"colors must be a list, got {type(colors).__name__}")
        if len(colors) != num_series:
            raise ValueError(f"Number of colors ({len(colors)}) must match number of series ({num_series})")
    
    if line_styles is not None:
        if not isinstance(line_styles, list):
            raise TypeError(f"line_styles must be a list, got {type(line_styles).__name__}")
        if len(line_styles) != num_series:
            raise ValueError(f"Number of line_styles ({len(line_styles)}) must match number of series ({num_series})")
    
    if markers is not None:
        if not isinstance(markers, list):
            raise TypeError(f"markers must be a list, got {type(markers).__name__}")
        if len(markers) != num_series:
            raise ValueError(f"Number of markers ({len(markers)}) must match number of series ({num_series})")

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    for i, y in enumerate(y_series):
        plot_kwargs: dict[str, Any] = {}
        
        if labels is not None:
            plot_kwargs['label'] = labels[i]
        if colors is not None:
            plot_kwargs['color'] = colors[i]
        if line_styles is not None:
            plot_kwargs['linestyle'] = line_styles[i]
        if markers is not None:
            plot_kwargs['marker'] = markers[i]
        
        ax.plot(x_data, y, **plot_kwargs)
    
    # Customize plot
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--')
    
    if legend and labels is not None:
        ax.legend(loc='best', framealpha=0.9)
    
    plt.tight_layout()
    
    logger.debug(f"Created line plot with {num_series} series and {len(x_data)} data points")
    
    return fig, ax


def create_scatter_plot(
    x_data: list[float] | np.ndarray,
    y_data: list[float] | np.ndarray,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    colors: list[str] | str | None = None,
    sizes: list[float] | float = 50,
    alpha: float = 0.6,
    grid: bool = True,
    figsize: tuple[int, int] = (10, 6),
    marker: str = 'o',
) -> tuple[Figure, Axes]:
    """
    Create a scatter plot with customizable styling.

    Parameters
    ----------
    x_data : list[float] | np.ndarray
        X-axis data points.
    y_data : list[float] | np.ndarray
        Y-axis data points.
    title : str, optional
        Plot title (by default "").
    xlabel : str, optional
        X-axis label (by default "").
    ylabel : str, optional
        Y-axis label (by default "").
    colors : list[str] | str | None, optional
        Point colors, can be single color or list (by default None).
    sizes : list[float] | float, optional
        Point sizes (by default 50).
    alpha : float, optional
        Transparency level between 0 and 1 (by default 0.6).
    grid : bool, optional
        Whether to show grid (by default True).
    figsize : tuple[int, int], optional
        Figure size as (width, height) in inches (by default (10, 6)).
    marker : str, optional
        Marker style (by default 'o').

    Returns
    -------
    tuple[Figure, Axes]
        Matplotlib figure and axes objects.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data dimensions don't match or parameters are invalid.

    Examples
    --------
    >>> x = np.random.randn(100)
    >>> y = 2 * x + np.random.randn(100) * 0.5
    >>> fig, ax = create_scatter_plot(
    ...     x, y,
    ...     title="Correlation Plot",
    ...     xlabel="Feature X",
    ...     ylabel="Feature Y",
    ...     colors='blue',
    ...     alpha=0.5
    ... )
    >>> plt.show()

    Notes
    -----
    This function provides a clean interface for creating scatter plots with
    automatic validation and sensible defaults.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is number of data points
    """
    # Type validation
    if not isinstance(x_data, (list, np.ndarray)):
        raise TypeError(f"x_data must be a list or numpy array, got {type(x_data).__name__}")
    if not isinstance(y_data, (list, np.ndarray)):
        raise TypeError(f"y_data must be a list or numpy array, got {type(y_data).__name__}")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")
    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if not isinstance(grid, bool):
        raise TypeError(f"grid must be a boolean, got {type(grid).__name__}")
    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError("figsize must be a tuple of two integers")
    if not isinstance(marker, str):
        raise TypeError(f"marker must be a string, got {type(marker).__name__}")

    # Convert to numpy arrays
    x_data = np.asarray(x_data)
    y_data = np.asarray(y_data)
    
    # Value validation
    if len(x_data) == 0:
        raise ValueError("x_data cannot be empty")
    if len(y_data) == 0:
        raise ValueError("y_data cannot be empty")
    if len(x_data) != len(y_data):
        raise ValueError(f"x_data length ({len(x_data)}) must match y_data length ({len(y_data)})")
    if not 0 <= alpha <= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {alpha}")
    if figsize[0] <= 0 or figsize[1] <= 0:
        raise ValueError(f"figsize dimensions must be positive, got {figsize}")

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    scatter = ax.scatter(x_data, y_data, c=colors, s=sizes, alpha=alpha, marker=marker)
    
    # Customize plot
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    logger.debug(f"Created scatter plot with {len(x_data)} data points")
    
    return fig, ax


def create_bar_plot(
    categories: list[str],
    values: list[float] | list[list[float]],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    labels: list[str] | None = None,
    colors: list[str] | None = None,
    horizontal: bool = False,
    stacked: bool = False,
    grid: bool = True,
    legend: bool = True,
    figsize: tuple[int, int] = (10, 6),
) -> tuple[Figure, Axes]:
    """
    Create a bar plot with support for grouped and stacked bars.

    Parameters
    ----------
    categories : list[str]
        Category names for the x-axis (or y-axis if horizontal).
    values : list[float] | list[list[float]]
        Values for each category. Can be single series or multiple series.
    title : str, optional
        Plot title (by default "").
    xlabel : str, optional
        X-axis label (by default "").
    ylabel : str, optional
        Y-axis label (by default "").
    labels : list[str] | None, optional
        Legend labels for each series (by default None).
    colors : list[str] | None, optional
        Colors for each series (by default None).
    horizontal : bool, optional
        Whether to create horizontal bars (by default False).
    stacked : bool, optional
        Whether to stack bars (by default False).
    grid : bool, optional
        Whether to show grid (by default True).
    legend : bool, optional
        Whether to show legend (by default True).
    figsize : tuple[int, int], optional
        Figure size as (width, height) in inches (by default (10, 6)).

    Returns
    -------
    tuple[Figure, Axes]
        Matplotlib figure and axes objects.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data dimensions don't match or are invalid.

    Examples
    --------
    >>> categories = ['Q1', 'Q2', 'Q3', 'Q4']
    >>> sales = [100, 150, 120, 180]
    >>> fig, ax = create_bar_plot(
    ...     categories, sales,
    ...     title="Quarterly Sales",
    ...     xlabel="Quarter",
    ...     ylabel="Sales ($K)"
    ... )
    >>> plt.show()

    >>> # Grouped bars
    >>> values = [[100, 150, 120, 180], [90, 140, 110, 170]]
    >>> fig, ax = create_bar_plot(
    ...     categories, values,
    ...     labels=["2023", "2024"],
    ...     title="Year-over-Year Comparison"
    ... )

    Notes
    -----
    Supports both single and multiple bar series with automatic positioning
    for grouped bars.

    Complexity
    ----------
    Time: O(n*m) where n is categories and m is number of series
    Space: O(n*m)
    """
    # Type validation
    if not isinstance(categories, list):
        raise TypeError(f"categories must be a list, got {type(categories).__name__}")
    if not isinstance(values, list):
        raise TypeError(f"values must be a list, got {type(values).__name__}")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")
    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")
    if not isinstance(horizontal, bool):
        raise TypeError(f"horizontal must be a boolean, got {type(horizontal).__name__}")
    if not isinstance(stacked, bool):
        raise TypeError(f"stacked must be a boolean, got {type(stacked).__name__}")
    if not isinstance(grid, bool):
        raise TypeError(f"grid must be a boolean, got {type(grid).__name__}")
    if not isinstance(legend, bool):
        raise TypeError(f"legend must be a boolean, got {type(legend).__name__}")
    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError("figsize must be a tuple of two integers")

    # Value validation
    if len(categories) == 0:
        raise ValueError("categories cannot be empty")
    if not all(isinstance(cat, str) for cat in categories):
        raise TypeError("All category items must be strings")
    if figsize[0] <= 0 or figsize[1] <= 0:
        raise ValueError(f"figsize dimensions must be positive, got {figsize}")

    # Handle multiple series
    if len(values) > 0 and isinstance(values[0], list):
        value_series = [list(v) for v in values]
    else:
        value_series = [list(values)]

    # Validate dimensions
    for i, series in enumerate(value_series):
        if len(series) != len(categories):
            raise ValueError(
                f"values series {i} length ({len(series)}) must match categories length ({len(categories)})"
            )

    num_series = len(value_series)

    # Validate optional parameters
    if labels is not None:
        if not isinstance(labels, list):
            raise TypeError(f"labels must be a list, got {type(labels).__name__}")
        if len(labels) != num_series:
            raise ValueError(f"Number of labels ({len(labels)}) must match number of series ({num_series})")
    
    if colors is not None:
        if not isinstance(colors, list):
            raise TypeError(f"colors must be a list, got {type(colors).__name__}")
        if len(colors) != num_series:
            raise ValueError(f"Number of colors ({len(colors)}) must match number of series ({num_series})")

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    x = np.arange(len(categories))
    width = 0.8 / num_series if not stacked else 0.8
    
    if stacked:
        # Stacked bars
        bottom = np.zeros(len(categories))
        for i, series in enumerate(value_series):
            plot_kwargs: dict[str, Any] = {'width': width}
            if labels is not None:
                plot_kwargs['label'] = labels[i]
            if colors is not None:
                plot_kwargs['color'] = colors[i]
            
            if horizontal:
                ax.barh(x, series, **plot_kwargs, left=bottom)
            else:
                ax.bar(x, series, **plot_kwargs, bottom=bottom)
            
            bottom += np.array(series)
    else:
        # Grouped bars
        for i, series in enumerate(value_series):
            offset = (i - num_series / 2 + 0.5) * width
            plot_kwargs: dict[str, Any] = {'width': width}
            if labels is not None:
                plot_kwargs['label'] = labels[i]
            if colors is not None:
                plot_kwargs['color'] = colors[i]
            
            if horizontal:
                ax.barh(x + offset, series, **plot_kwargs)
            else:
                ax.bar(x + offset, series, **plot_kwargs)
    
    # Set ticks and labels
    if horizontal:
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        if grid:
            ax.grid(True, alpha=0.3, linestyle='--', axis='x')
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        if grid:
            ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    
    if legend and labels is not None:
        ax.legend(loc='best', framealpha=0.9)
    
    plt.tight_layout()
    
    logger.debug(f"Created bar plot with {len(categories)} categories and {num_series} series")
    
    return fig, ax


def create_histogram(
    data: list[float] | np.ndarray | list[list[float]] | list[np.ndarray],
    bins: int | str = 'auto',
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
    labels: list[str] | None = None,
    colors: list[str] | None = None,
    alpha: float = 0.7,
    density: bool = False,
    cumulative: bool = False,
    grid: bool = True,
    legend: bool = True,
    figsize: tuple[int, int] = (10, 6),
) -> tuple[Figure, Axes]:
    """
    Create a histogram with support for multiple distributions.

    Parameters
    ----------
    data : list[float] | np.ndarray | list[list[float]] | list[np.ndarray]
        Data to plot. Can be single dataset or multiple datasets.
    bins : int | str, optional
        Number of bins or binning strategy ('auto', 'sturges', 'scott', etc.) (by default 'auto').
    title : str, optional
        Plot title (by default "").
    xlabel : str, optional
        X-axis label (by default "").
    ylabel : str, optional
        Y-axis label (by default "Frequency").
    labels : list[str] | None, optional
        Legend labels for each dataset (by default None).
    colors : list[str] | None, optional
        Colors for each dataset (by default None).
    alpha : float, optional
        Transparency level between 0 and 1 (by default 0.7).
    density : bool, optional
        Whether to normalize to create a probability density (by default False).
    cumulative : bool, optional
        Whether to create cumulative histogram (by default False).
    grid : bool, optional
        Whether to show grid (by default True).
    legend : bool, optional
        Whether to show legend (by default True).
    figsize : tuple[int, int], optional
        Figure size as (width, height) in inches (by default (10, 6)).

    Returns
    -------
    tuple[Figure, Axes]
        Matplotlib figure and axes objects.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters are invalid.

    Examples
    --------
    >>> data = np.random.randn(1000)
    >>> fig, ax = create_histogram(
    ...     data,
    ...     bins=30,
    ...     title="Normal Distribution",
    ...     xlabel="Value",
    ...     alpha=0.8
    ... )
    >>> plt.show()

    >>> # Multiple distributions
    >>> data1 = np.random.randn(1000)
    >>> data2 = np.random.randn(1000) + 2
    >>> fig, ax = create_histogram(
    ...     [data1, data2],
    ...     labels=["Group A", "Group B"],
    ...     alpha=0.6
    ... )

    Notes
    -----
    Automatically handles multiple distributions with proper overlap visualization.

    Complexity
    ----------
    Time: O(n*log(n)) for binning, Space: O(n) where n is data size
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(bins, (int, str)):
        raise TypeError(f"bins must be an integer or string, got {type(bins).__name__}")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")
    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if not isinstance(density, bool):
        raise TypeError(f"density must be a boolean, got {type(density).__name__}")
    if not isinstance(cumulative, bool):
        raise TypeError(f"cumulative must be a boolean, got {type(cumulative).__name__}")
    if not isinstance(grid, bool):
        raise TypeError(f"grid must be a boolean, got {type(grid).__name__}")
    if not isinstance(legend, bool):
        raise TypeError(f"legend must be a boolean, got {type(legend).__name__}")
    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError("figsize must be a tuple of two integers")

    # Value validation
    if isinstance(bins, int) and bins <= 0:
        raise ValueError(f"bins must be positive, got {bins}")
    if not 0 <= alpha <= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {alpha}")
    if figsize[0] <= 0 or figsize[1] <= 0:
        raise ValueError(f"figsize dimensions must be positive, got {figsize}")

    # Handle multiple datasets
    if isinstance(data, np.ndarray) and data.ndim == 1:
        datasets = [data]
    elif isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], (list, np.ndarray)):
            datasets = [np.asarray(d) for d in data]
        else:
            datasets = [np.asarray(data)]
    else:
        datasets = [np.asarray(data)]

    # Validate datasets
    for i, dataset in enumerate(datasets):
        if len(dataset) == 0:
            raise ValueError(f"dataset {i} cannot be empty")

    num_datasets = len(datasets)

    # Validate optional parameters
    if labels is not None:
        if not isinstance(labels, list):
            raise TypeError(f"labels must be a list, got {type(labels).__name__}")
        if len(labels) != num_datasets:
            raise ValueError(f"Number of labels ({len(labels)}) must match number of datasets ({num_datasets})")
    
    if colors is not None:
        if not isinstance(colors, list):
            raise TypeError(f"colors must be a list, got {type(colors).__name__}")
        if len(colors) != num_datasets:
            raise ValueError(f"Number of colors ({len(colors)}) must match number of datasets ({num_datasets})")

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    for i, dataset in enumerate(datasets):
        hist_kwargs: dict[str, Any] = {
            'bins': bins,
            'alpha': alpha,
            'density': density,
            'cumulative': cumulative,
        }
        
        if labels is not None:
            hist_kwargs['label'] = labels[i]
        if colors is not None:
            hist_kwargs['color'] = colors[i]
        
        ax.hist(dataset, **hist_kwargs)
    
    # Customize plot
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    if legend and labels is not None:
        ax.legend(loc='best', framealpha=0.9)
    
    plt.tight_layout()
    
    total_points = sum(len(d) for d in datasets)
    logger.debug(f"Created histogram with {num_datasets} datasets and {total_points} total data points")
    
    return fig, ax


__all__ = [
    'create_line_plot',
    'create_scatter_plot',
    'create_bar_plot',
    'create_histogram',
]
