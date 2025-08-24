import pandas as pd


def sort_df_columns(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """Sort the columns of ``df`` alphabetically.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose columns will be sorted.
    ascending : bool, optional
        Sort columns in ascending order, by default ``True``.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns reordered alphabetically.
    """
    sorted_cols = sorted(df.columns, reverse=not ascending)
    return df[sorted_cols]


__all__ = ["sort_df_columns"]
