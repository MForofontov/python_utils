import pandas as pd


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = "inner") -> pd.DataFrame:
    """Merge two pandas DataFrames on a common column.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame to merge.
    df2 : pd.DataFrame
        The second DataFrame to merge.
    on : str
        Column name to join on.
    how : str, optional
        Type of merge to perform, by default ``"inner"``.

    Returns
    -------
    pd.DataFrame
        The merged DataFrame.

    Raises
    ------
    KeyError
        If ``on`` is not present in both ``df1`` and ``df2``.
    """

    if on not in df1.columns:
        raise KeyError(f"Column '{on}' not found in first DataFrame")
    if on not in df2.columns:
        raise KeyError(f"Column '{on}' not found in second DataFrame")
    return pd.merge(df1, df2, on=on, how=how)


__all__ = ["merge_dataframes"]
