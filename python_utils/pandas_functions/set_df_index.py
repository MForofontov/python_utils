import pandas as pd
from collections.abc import Iterable


def set_df_index(
    df: pd.DataFrame, columns: Iterable[str], drop: bool = True
) -> pd.DataFrame:
    """Return ``df`` with ``columns`` set as the index.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to modify.
    columns : Iterable[str]
        Column names to set as the new index.
    drop : bool, default True
        Whether to delete ``columns`` from ``df``.

    Returns
    -------
    pd.DataFrame
        DataFrame with ``columns`` as index.

    Raises
    ------
    KeyError
        If any of ``columns`` do not exist in ``df``.
    """
    columns_list = list(columns)
    missing = set(columns_list) - set(df.columns)
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return df.set_index(columns_list, drop=drop)


__all__ = ["set_df_index"]
