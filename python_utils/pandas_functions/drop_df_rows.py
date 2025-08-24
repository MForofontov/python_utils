import pandas as pd
from collections.abc import Iterable


def drop_df_rows(df: pd.DataFrame, indices: Iterable[object]) -> pd.DataFrame:
    """Return ``df`` with specified index labels removed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to drop rows from.
    indices : Iterable[object]
        Index labels to remove.

    Returns
    -------
    pd.DataFrame
        A DataFrame without the specified rows.

    Raises
    ------
    KeyError
        If any of ``indices`` are not present in ``df.index``.
    """
    indices_list = list(indices)
    missing = set(indices_list) - set(df.index)
    if missing:
        raise KeyError(f"Index labels not found: {missing}")
    return df.drop(index=indices_list)


__all__ = ["drop_df_rows"]
