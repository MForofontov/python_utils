import pandas as pd
from collections.abc import Iterable


def split_df_column(df: pd.DataFrame, column: str, into: Iterable[str], sep: str) -> pd.DataFrame:
    """Split a column into multiple new columns using a separator.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column to split.
    column : str
        Name of the column to split.
    into : Iterable[str]
        Names of the columns to create from the split values.
    sep : str
        Separator used to split the column values.

    Returns
    -------
    pd.DataFrame
        DataFrame with the original column removed and new columns added.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    ValueError
        If the number of resulting columns does not match ``into``.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")
    into_list = list(into)
    new_columns = df[column].astype(str).str.split(sep, expand=True)
    if new_columns.shape[1] != len(into_list):
        raise ValueError("Number of resulting columns does not match 'into'")
    new_columns.columns = into_list
    return df.drop(columns=[column]).join(new_columns)


__all__ = ["split_df_column"]
