import pandas as pd


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = "inner") -> pd.DataFrame:
    """Merge two pandas DataFrames.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame to merge.
    df2 : pd.DataFrame
        The second DataFrame to merge.
    on : str
        Column name to join on.
    how : str, optional
        Type of merge to perform, by default "inner".

    Returns
    -------
    pd.DataFrame
        The merged DataFrame.
    """
    return pd.merge(df1, df2, on=on, how=how)


__all__ = ["merge_dataframes"]
