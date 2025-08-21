import pandas as pd
from collections.abc import Iterable
from typing import Literal


def drop_duplicate_df_rows(
    df: pd.DataFrame,
    subset: Iterable[str] | None = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.DataFrame:
    """Return ``df`` with duplicate rows removed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to remove duplicates from.
    subset : Iterable[str] | None, optional
        Columns to consider when identifying duplicates. If ``None``,
        all columns are used.
    keep : {"first", "last", False}, optional
        Which duplicate to keep. Default is ``"first"``.

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicate rows removed.

    Raises
    ------
    ValueError
        If ``keep`` is not one of ``"first"``, ``"last"`` or ``False``.
    """
    if keep not in {"first", "last", False}:
        raise ValueError("keep must be 'first', 'last' or False")
    subset_list = list(subset) if subset is not None else None
    return df.drop_duplicates(subset=subset_list, keep=keep)


__all__ = ["drop_duplicate_df_rows"]
