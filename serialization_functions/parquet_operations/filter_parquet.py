"""
Filter Parquet file by column values.
"""

from typing import Any


def filter_parquet(
    file_path: str,
    filters: list[tuple[str, str, Any]],
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Read Parquet file with filtering conditions.

    Parameters
    ----------
    file_path : str
        Path to Parquet file.
    filters : list[tuple[str, str, Any]]
        List of (column, operator, value) tuples. Operators: '=', '!=', '<', '>', '<=', '>=', 'in', 'not in'.
    columns : list[str] | None, optional
        Specific columns to read (by default None for all).

    Returns
    -------
    list[dict[str, Any]]
        Filtered list of dictionaries.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If filters have invalid format.
    FileNotFoundError
        If file doesn't exist.
    ImportError
        If pyarrow is not installed.

    Examples
    --------
    >>> filters = [('age', '>', 25), ('name', '!=', 'Bob')]
    >>> data = filter_parquet('people.parquet', filters)

    >>> filters = [('city', 'in', ['NYC', 'LA'])]
    >>> data = filter_parquet('people.parquet', filters, columns=['name', 'city'])

    Notes
    -----
    Requires pyarrow package.
    Pushdown filtering for efficiency.

    Complexity
    ----------
    Time: O(n*m), Space: O(k*m), where n is rows, m is columns, k is filtered rows
    """
    try:
        import pyarrow.parquet as pq
        import pyarrow.compute as pc
    except ImportError as e:
        raise ImportError("pyarrow is required. Install with: pip install pyarrow") from e
    
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
    
    if not isinstance(filters, list):
        raise TypeError(f"filters must be a list, got {type(filters).__name__}")
    
    if columns is not None:
        if not isinstance(columns, list):
            raise TypeError(f"columns must be a list or None, got {type(columns).__name__}")
    
    # Validate filters
    for f in filters:
        if not isinstance(f, tuple) or len(f) != 3:
            raise ValueError("Each filter must be a tuple of (column, operator, value)")
        col, op, val = f
        if not isinstance(col, str):
            raise ValueError("Filter column must be a string")
        if not isinstance(op, str):
            raise ValueError("Filter operator must be a string")
    
    # Read table
    table = pq.read_table(file_path, columns=columns)
    
    # Apply filters
    mask = None
    for col, op, val in filters:
        column = table.column(col)
        
        if op == '=':
            condition = pc.equal(column, val)
        elif op == '!=':
            condition = pc.not_equal(column, val)
        elif op == '<':
            condition = pc.less(column, val)
        elif op == '>':
            condition = pc.greater(column, val)
        elif op == '<=':
            condition = pc.less_equal(column, val)
        elif op == '>=':
            condition = pc.greater_equal(column, val)
        elif op == 'in':
            if not isinstance(val, (list, tuple)):
                raise ValueError(f"Value for 'in' operator must be list or tuple, got {type(val).__name__}")
            condition = pc.is_in(column, val)
        elif op == 'not in':
            if not isinstance(val, (list, tuple)):
                raise ValueError(f"Value for 'not in' operator must be list or tuple, got {type(val).__name__}")
            condition = pc.invert(pc.is_in(column, val))
        else:
            raise ValueError(f"Unsupported operator: {op}")
        
        if mask is None:
            mask = condition
        else:
            mask = pc.and_(mask, condition)
    
    # Filter table
    if mask is not None:
        filtered_table = table.filter(mask)
    else:
        filtered_table = table
    
    return filtered_table.to_pylist()


__all__ = ['filter_parquet']
