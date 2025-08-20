import pandas as pd
from typing import Sequence


def concat_dfs(
    dfs: Sequence[pd.DataFrame],
    axis: int = 0,
    ignore_index: bool = False,
) -> pd.DataFrame:
    """Concatenate a sequence of DataFrames.

    Parameters
    ----------
    dfs : Sequence[pd.DataFrame]
        Sequence of DataFrames to concatenate. Must contain at least one DataFrame.
    axis : int, optional
        Axis along which to concatenate. By default 0.
    ignore_index : bool, optional
        If ``True``, ignore the index of the DataFrames. By default ``False``.

    Returns
    -------
    pd.DataFrame
        The concatenated DataFrame.

    Raises
    ------
    ValueError
        If ``dfs`` is empty.
    """
    if not dfs:
        raise ValueError("dfs must be a non-empty sequence of DataFrames")
    return pd.concat(dfs, axis=axis, ignore_index=ignore_index)


__all__ = ["concat_dfs"]
