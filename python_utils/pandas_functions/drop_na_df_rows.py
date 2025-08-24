import pandas as pd
from collections.abc import Iterable


def drop_na_df_rows(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Drop rows with missing values from ``df``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to drop rows from.
    columns : Iterable[str] | None, optional
        Columns to consider when identifying NA values. If ``None``, all columns are used.

    Returns
    -------
    pd.DataFrame
        DataFrame with rows containing NA values removed.

    Raises
    ------
    KeyError
        If any of ``columns`` are not present in ``df``.
    """
    if columns is not None:
        columns_list = list(columns)
        missing = set(columns_list) - set(df.columns)
        if missing:
            raise KeyError(f"Columns not found: {missing}")
    else:
        columns_list = None
    return df.dropna(subset=columns_list)


__all__ = ["drop_na_df_rows"]
