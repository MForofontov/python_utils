import pandas as pd


def reset_df_index(df: pd.DataFrame, drop: bool = False) -> pd.DataFrame:
    """Return ``df`` with its index reset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose index will be reset.
    drop : bool, default False
        If True, do not insert the index into the DataFrame columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with a new sequential index.
    """
    return df.reset_index(drop=drop)


__all__ = ["reset_df_index"]
