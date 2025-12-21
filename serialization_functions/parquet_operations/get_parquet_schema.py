"""
Get Parquet schema information.
"""

import pyarrow.parquet as pq


def get_parquet_schema(file_path: str) -> dict[str, str]:
    """
    Get schema (column names and types) from Parquet file.

    Parameters
    ----------
    file_path : str
        Path to Parquet file.

    Returns
    -------
    dict[str, str]
        Dictionary mapping column names to Arrow type strings.

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
    >>> schema = get_parquet_schema('people.parquet')
    >>> schema
    {'name': 'string', 'age': 'int64'}

    Notes
    -----
    Requires pyarrow package.
    Returns Arrow data types as strings.

    Complexity
    ----------
    Time: O(m), Space: O(m), where m is number of columns
    """
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
    
    # Read schema
    parquet_file = pq.ParquetFile(file_path)
    schema = parquet_file.schema_arrow
    
    return {field.name: str(field.type) for field in schema}


__all__ = ['get_parquet_schema']
