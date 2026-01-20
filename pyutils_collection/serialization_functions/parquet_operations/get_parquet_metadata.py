"""
Get Parquet file metadata.
"""

from typing import Any

import pyarrow.parquet as pq


def get_parquet_metadata(file_path: str) -> dict[str, Any]:
    """
    Get metadata from Parquet file.

    Parameters
    ----------
    file_path : str
        Path to Parquet file.

    Returns
    -------
    dict[str, Any]
        Dictionary containing metadata: num_rows, num_columns, schema, etc.

    Raises
    ------
    TypeError
        If file_path is not a string.
    FileNotFoundError
        If file doesn't exist.
    ImportError
        If pyarrow is not installed.

    Examples
    --------
    >>> metadata = get_parquet_metadata('people.parquet')
    >>> metadata['num_rows']
    2
    >>> metadata['columns']
    ['name', 'age']

    Notes
    -----
    Requires pyarrow package.
    Reads metadata without loading full file.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")

    # Read metadata
    parquet_file = pq.ParquetFile(file_path)
    metadata = parquet_file.metadata
    schema = parquet_file.schema

    return {
        "num_rows": metadata.num_rows,
        "num_columns": metadata.num_columns,
        "num_row_groups": metadata.num_row_groups,
        "columns": schema.names,
        "schema": str(schema),
        "serialized_size": metadata.serialized_size,
    }


__all__ = ["get_parquet_metadata"]
