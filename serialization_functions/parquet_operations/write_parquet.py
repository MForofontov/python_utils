"""
Write data to Parquet file.
"""

from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq


def write_parquet(
    data: list[dict[str, Any]],
    file_path: str,
    compression: str = "snappy",
) -> None:
    """
    Write list of dictionaries to Parquet file.

    Parameters
    ----------
    data : list[dict[str, Any]]
        List of dictionaries with consistent schema.
    file_path : str
        Path to output Parquet file.
    compression : str, optional
        Compression codec: 'none', 'snappy', 'gzip', 'brotli', 'lz4', 'zstd' (by default "snappy").

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or has inconsistent schema.
    ImportError
        If pyarrow is not installed.

    Examples
    --------
    >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    >>> write_parquet(data, 'people.parquet')

    >>> write_parquet(data, 'people.parquet', compression='gzip')

    Notes
    -----
    Requires pyarrow package.
    Parquet is columnar format, efficient for analytics.
    Creates parent directories if they don't exist.

    Complexity
    ----------
    Time: O(n*m), Space: O(n*m), where n is rows, m is columns
    """
    if not isinstance(data, list):
        raise TypeError(f"data must be a list, got {type(data).__name__}")

    if not data:
        raise ValueError("data cannot be empty")

    if not all(isinstance(item, dict) for item in data):
        raise TypeError("all elements in data must be dictionaries")

    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")

    if not isinstance(compression, str):
        raise TypeError(
            f"compression must be a string, got {type(compression).__name__}"
        )

    valid_compressions = {"none", "snappy", "gzip", "brotli", "lz4", "zstd"}
    if compression.lower() not in valid_compressions:
        raise ValueError(
            f"compression must be one of {valid_compressions}, got '{compression}'"
        )

    # Create parent directories
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    # Convert to PyArrow Table
    try:
        table = pa.Table.from_pylist(data)
    except Exception as e:
        raise ValueError(f"Failed to convert data to Arrow table: {e}") from e

    # Write to Parquet
    pq.write_table(
        table,
        file_path,
        compression=compression.upper() if compression != "none" else None,
    )


__all__ = ["write_parquet"]
