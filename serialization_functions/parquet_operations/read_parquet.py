"""
Read Parquet file into list of dictionaries.
"""

from typing import Any


def read_parquet(
    file_path: str,
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Read Parquet file into list of dictionaries.

    Parameters
    ----------
    file_path : str
        Path to Parquet file.
    columns : list[str] | None, optional
        Specific columns to read (by default None for all).

    Returns
    -------
    list[dict[str, Any]]
        List of dictionaries, one per row.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If file doesn't exist.
    ImportError
        If pyarrow is not installed.

    Examples
    --------
    >>> data = read_parquet('people.parquet')
    >>> data[0]
    {'name': 'Alice', 'age': 30}

    >>> data = read_parquet('people.parquet', columns=['name'])
    >>> data[0]
    {'name': 'Alice'}

    Notes
    -----
    Requires pyarrow package.
    Efficient columnar reading.

    Complexity
    ----------
    Time: O(n*m), Space: O(n*m), where n is rows, m is columns
    """
    try:
        import pyarrow.parquet as pq
    except ImportError as e:
        raise ImportError("pyarrow is required. Install with: pip install pyarrow") from e
    
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
    
    if columns is not None:
        if not isinstance(columns, list):
            raise TypeError(f"columns must be a list or None, got {type(columns).__name__}")
        if not all(isinstance(col, str) for col in columns):
            raise TypeError("all elements in columns must be strings")
    
    # Read Parquet file
    table = pq.read_table(file_path, columns=columns)
    
    # Convert to list of dicts
    return table.to_pylist()


__all__ = ['read_parquet']
