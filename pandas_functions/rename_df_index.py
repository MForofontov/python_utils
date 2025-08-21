import pandas as pd
from collections.abc import Hashable


def rename_df_index(df: pd.DataFrame, index_map: dict[Hashable, Hashable]) -> pd.DataFrame:
    """Rename index labels of ``df`` according to ``index_map``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose index will be renamed.
    index_map : dict[Hashable, Hashable]
        Mapping of existing index labels to new labels.

    Returns
    -------
    pd.DataFrame
        DataFrame with renamed index labels.

    Raises
    ------
    KeyError
        If any keys in ``index_map`` are not present in ``df.index``.
    """
    missing = set(index_map) - set(df.index)
    if missing:
        raise KeyError(f"Index labels not found: {missing}")
    return df.rename(index=index_map)


__all__ = ["rename_df_index"]
