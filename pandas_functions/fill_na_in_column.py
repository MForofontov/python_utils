import pandas as pd
from typing import Any


def fill_na_in_column(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """Fill missing values in a specific column with ``value``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column to modify.
    column : str
        Name of the column in which ``NaN`` values will be filled.
    value : Any
        Value to replace ``NaN`` entries with.

    Returns
    -------
    pd.DataFrame
        A new DataFrame where ``NaN`` values in ``column`` are replaced by ``value``.

    Raises
    ------
    KeyError
        If ``column`` does not exist in ``df``.
    """

    if column not in df.columns:
        raise KeyError(column)
    result = df.copy()
    result[column] = result[column].fillna(value)
    return result


__all__ = ["fill_na_in_column"]

