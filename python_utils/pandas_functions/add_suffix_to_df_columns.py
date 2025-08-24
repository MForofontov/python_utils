import pandas as pd


def add_suffix_to_df_columns(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    """Add ``suffix`` to each column name of ``df``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose column names will be modified.
    suffix : str
        Suffix to append to each column name.

    Returns
    -------
    pd.DataFrame
        DataFrame with updated column names.
    """
    return df.add_suffix(suffix)


__all__ = ["add_suffix_to_df_columns"]
