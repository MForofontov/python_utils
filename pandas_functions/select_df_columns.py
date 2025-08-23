import pandas as pd
from collections.abc import Iterable


def select_df_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Return a DataFrame with only the specified columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to select columns from.
    columns : Iterable[str]
        Column names to include in the returned DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing only ``columns`` in the order provided.

    Raises
    ------
    KeyError
        If any of ``columns`` are not present in ``df``.
    """

    columns_list = list(columns)
    missing = set(columns_list) - set(df.columns)
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return df[columns_list]


__all__ = ["select_df_columns"]
