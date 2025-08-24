import pandas as pd


def rename_df_columns(df: pd.DataFrame, columns_map: dict[str, str]) -> pd.DataFrame:
    """Rename columns of ``df`` according to ``columns_map``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose columns will be renamed.
    columns_map : dict[str, str]
        Mapping of existing column names to new names.

    Returns
    -------
    pd.DataFrame
        DataFrame with renamed columns.

    Raises
    ------
    KeyError
        If any keys in ``columns_map`` are not present in ``df``.
    """

    missing = set(columns_map) - set(df.columns)
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return df.rename(columns=columns_map)


__all__ = ["rename_df_columns"]
