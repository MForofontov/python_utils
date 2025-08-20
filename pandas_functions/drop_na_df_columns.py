import pandas as pd


def drop_na_df_columns(df: pd.DataFrame, how: str = "any") -> pd.DataFrame:
    """Remove columns from ``df`` that contain NA values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to drop columns from.
    how : {"any", "all"}, default "any"
        Determine whether to drop a column if it contains any NA values
        or only if all values are NA.

    Returns
    -------
    pd.DataFrame
        DataFrame without columns containing NA values.
    """
    return df.dropna(axis=1, how=how)


__all__ = ["drop_na_df_columns"]
