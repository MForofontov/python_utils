import pandas as pd


def explode_df_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Explode a column containing list-like elements into separate rows.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to operate on.
    column : str
        Name of the column containing list-like objects to explode.

    Returns
    -------
    pd.DataFrame
        DataFrame with the specified column exploded and index reset.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")
    return df.explode(column, ignore_index=True)


__all__ = ["explode_df_column"]
