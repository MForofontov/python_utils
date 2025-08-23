import pandas as pd
from collections.abc import Sequence
from typing import Union


def sort_df_by_columns(
    df: pd.DataFrame, columns: Union[str, Sequence[str]], ascending: Union[bool, Sequence[bool]] = True
) -> pd.DataFrame:
    """Sort a DataFrame by one or more columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to sort.
    columns : Union[str, Sequence[str]]
        Column name or names to sort by.
    ascending : Union[bool, Sequence[bool]], optional
        Sort ascending or descending for each column, by default ``True``.

    Returns
    -------
    pd.DataFrame
        The sorted DataFrame.

    Raises
    ------
    KeyError
        If any of ``columns`` are not present in ``df``.
    """

    cols = [columns] if isinstance(columns, str) else list(columns)
    missing = set(cols) - set(df.columns)
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return df.sort_values(by=columns, ascending=ascending)


__all__ = ["sort_df_by_columns"]
