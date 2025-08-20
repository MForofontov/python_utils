import pandas as pd


def convert_df_column_dtype(df: pd.DataFrame, column: str, dtype: str | type) -> pd.DataFrame:
    """Convert ``column`` of ``df`` to ``dtype``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column to convert.
    column : str
        Name of the column to convert.
    dtype : str | type
        Target data type for the column.

    Returns
    -------
    pd.DataFrame
        DataFrame with the converted column.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(column)
    result = df.copy()
    result[column] = result[column].astype(dtype)
    return result


__all__ = ["convert_df_column_dtype"]
