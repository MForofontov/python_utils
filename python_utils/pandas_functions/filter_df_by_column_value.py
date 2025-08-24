import pandas as pd
from typing import Any


def filter_df_by_column_value(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """Filter a DataFrame based on a column's value.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    column : str
        Name of the column to filter on.
    value : Any
        Value to match in the specified column.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing only rows where ``column`` equals ``value``.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(column)
    return df[df[column] == value]


__all__ = ["filter_df_by_column_value"]
