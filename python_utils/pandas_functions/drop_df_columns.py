import pandas as pd
from collections.abc import Iterable


def drop_df_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Return a DataFrame with ``columns`` removed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to drop columns from.
    columns : Iterable[str]
        Column names to remove.

    Returns
    -------
    pd.DataFrame
        A DataFrame that does not include ``columns``.

    Raises
    ------
    KeyError
        If any of ``columns`` are not present in ``df``.
    """

    columns_list = list(columns)
    missing = set(columns_list) - set(df.columns)
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return df.drop(columns=columns_list)


__all__ = ["drop_df_columns"]
