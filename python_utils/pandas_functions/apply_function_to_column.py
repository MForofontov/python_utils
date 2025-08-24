import pandas as pd
from collections.abc import Callable
from typing import Any


def apply_function_to_column(df: pd.DataFrame, column: str, func: Callable[[Any], Any]) -> pd.DataFrame:
    """Apply ``func`` to ``column`` of ``df``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose column will be modified.
    column : str
        Name of the column to apply ``func`` to.
    func : Callable[[Any], Any]
        Function to apply to each element of the column.

    Returns
    -------
    pd.DataFrame
        DataFrame with the modified column.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(column)
    result = df.copy()
    result[column] = result[column].apply(func)
    return result


__all__ = ["apply_function_to_column"]
