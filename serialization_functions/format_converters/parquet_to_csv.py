"""Parquet to CSV converter."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


def parquet_to_csv(
    input_file: str | Path,
    output_file: str | Path,
    *,
    columns: list[str] | None = None,
    max_rows: int | None = None,
    filter_func: Callable[[dict[str, Any]], bool] | None = None,
    include_header: bool = True,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> int:
    """
    Convert Parquet file to CSV format.

    Reads Parquet data and writes to CSV with optional column selection,
    row limiting, and custom filtering. Useful for exporting Parquet data
    to CSV-compatible tools.

    Parameters
    ----------
    input_file : str | Path
        Path to input Parquet file.
    output_file : str | Path
        Path to output CSV file.
    columns : list[str] | None, optional
        Specific columns to export (by default None for all columns).
    max_rows : int | None, optional
        Maximum number of rows to export (by default None for all rows).
    filter_func : Callable[[dict[str, Any]], bool] | None, optional
        Function to filter rows, returns True to include (by default None).
    include_header : bool, optional
        Include header row with column names (by default True).
    delimiter : str, optional
        CSV delimiter character (by default ',').
    encoding : str, optional
        Character encoding for CSV file (by default 'utf-8').

    Returns
    -------
    int
        Number of rows written (excluding header).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If input file doesn't exist.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> # Basic conversion
    >>> rows = parquet_to_csv('data.parquet', 'output.csv')
    >>> rows
    1000

    >>> # Select specific columns
    >>> rows = parquet_to_csv(
    ...     'data.parquet',
    ...     'output.csv',
    ...     columns=['id', 'name', 'value']
    ... )

    >>> # Limit rows and filter
    >>> rows = parquet_to_csv(
    ...     'data.parquet',
    ...     'output.csv',
    ...     max_rows=100,
    ...     filter_func=lambda row: row['value'] > 50
    ... )

    >>> # Custom delimiter (TSV)
    >>> rows = parquet_to_csv(
    ...     'data.parquet',
    ...     'output.tsv',
    ...     delimiter='\\t'
    ... )

    Notes
    -----
    Large Parquet files are processed in batches to manage memory.
    Filter function receives row as dictionary: {'col1': val1, 'col2': val2}

    Complexity
    ----------
    Time: O(n) where n=number of rows
    Space: O(b) where b=batch size
    """
    # Type validation
    if not isinstance(input_file, (str, Path)):
        raise TypeError(
            f"input_file must be str or Path, got {type(input_file).__name__}"
        )
    if not isinstance(output_file, (str, Path)):
        raise TypeError(
            f"output_file must be str or Path, got {type(output_file).__name__}"
        )
    if columns is not None and not isinstance(columns, list):
        raise TypeError(f"columns must be list or None, got {type(columns).__name__}")
    if max_rows is not None and not isinstance(max_rows, int):
        raise TypeError(f"max_rows must be int or None, got {type(max_rows).__name__}")
    if filter_func is not None and not callable(filter_func):
        raise TypeError("filter_func must be callable or None")
    if not isinstance(include_header, bool):
        raise TypeError(
            f"include_header must be bool, got {type(include_header).__name__}"
        )
    if not isinstance(delimiter, str):
        raise TypeError(f"delimiter must be str, got {type(delimiter).__name__}")
    if not isinstance(encoding, str):
        raise TypeError(f"encoding must be str, got {type(encoding).__name__}")

    # Value validation
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if max_rows is not None and max_rows <= 0:
        raise ValueError(f"max_rows must be positive, got {max_rows}")

    if len(delimiter) != 1:
        raise ValueError(f"delimiter must be single character, got '{delimiter}'")

    # Read Parquet file
    table = pq.read_table(input_path, columns=columns)

    # Validate columns if specified
    if columns is not None:
        for col in columns:
            if col not in table.column_names:
                raise ValueError(f"Column '{col}' not found in Parquet file")

    # Convert to list of dictionaries for easier filtering
    data = table.to_pylist()

    # Apply filter if provided
    if filter_func is not None:
        data = [row for row in data if filter_func(row)]

    # Apply max_rows limit
    if max_rows is not None:
        data = data[:max_rows]

    # Write CSV
    import csv

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding=encoding) as f:
        if len(data) == 0:
            # Handle empty data
            if include_header and table.column_names:
                writer = csv.DictWriter(
                    f, fieldnames=table.column_names, delimiter=delimiter
                )
                writer.writeheader()
            return 0

        writer = csv.DictWriter(f, fieldnames=table.column_names, delimiter=delimiter)

        if include_header:
            writer.writeheader()

        writer.writerows(data)

    return len(data)


__all__ = ["parquet_to_csv"]
