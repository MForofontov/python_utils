import pandas as pd


def sort_df_by_index(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """Sort ``df`` by its index.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to sort by index.
    ascending : bool, optional
        Sort order. ``True`` for ascending, ``False`` for descending.

    Returns
    -------
    pd.DataFrame
        DataFrame sorted by index.
    """
    return df.sort_index(ascending=ascending)


__all__ = ["sort_df_by_index"]
