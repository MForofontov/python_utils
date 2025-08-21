import pandas as pd


def add_prefix_to_df_columns(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """Add ``prefix`` to each column name of ``df``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose column names will be modified.
    prefix : str
        Prefix to prepend to each column name.

    Returns
    -------
    pd.DataFrame
        DataFrame with updated column names.
    """
    return df.add_prefix(prefix)


__all__ = ["add_prefix_to_df_columns"]
