import pandas as pd
from collections.abc import Iterable
from typing import Any


def filter_df_by_column_values(
    df: pd.DataFrame, column: str, values: Iterable[Any]
) -> pd.DataFrame:
    """Filter a DataFrame based on multiple values in a column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    column : str
        Name of the column to filter on.
    values : Iterable[Any]
        Collection of values to match in the specified column.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing only rows where ``column`` equals any value in ``values``.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(column)
    return df[df[column].isin(values)]


__all__ = ["filter_df_by_column_values"]
