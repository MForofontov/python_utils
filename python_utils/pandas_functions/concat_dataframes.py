import pandas as pd
from collections.abc import Iterable


def concat_dataframes(dfs: Iterable[pd.DataFrame], axis: int = 0, ignore_index: bool = True) -> pd.DataFrame:
    """Concatenate an iterable of pandas DataFrames.

    Parameters
    ----------
    dfs : Iterable[pd.DataFrame]
        Sequence of DataFrames to concatenate.
    axis : int, optional
        Axis to concatenate along, by default ``0``.
    ignore_index : bool, optional
        Whether to ignore the index in the result, by default ``True``.

    Returns
    -------
    pd.DataFrame
        The concatenated DataFrame.

    Raises
    ------
    TypeError
        If any element in ``dfs`` is not a pandas DataFrame.
    ValueError
        If ``dfs`` is empty.
    """
    dfs_list = list(dfs)
    if not dfs_list:
        raise ValueError("dfs must contain at least one DataFrame")
    if not all(isinstance(df, pd.DataFrame) for df in dfs_list):
        raise TypeError("All items in dfs must be pandas DataFrames")
    return pd.concat(dfs_list, axis=axis, ignore_index=ignore_index)


__all__ = ["concat_dataframes"]
