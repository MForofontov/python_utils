import pandas as pd
from collections.abc import Iterable, Callable


def pivot_df(
    df: pd.DataFrame,
    index: str | Iterable[str],
    columns: str | Iterable[str],
    values: str,
    aggfunc: Callable | str = "mean",
    fill_value: object | None = None,
) -> pd.DataFrame:
    """Create a pivot table from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    index : str or Iterable[str]
        Column(s) to use as the new index.
    columns : str or Iterable[str]
        Column(s) to use to make new columns.
    values : str
        Column to aggregate.
    aggfunc : Callable or str, optional
        Aggregation function, by default ``"mean"``.
    fill_value : object, optional
        Value to replace missing entries with, by default ``None``.

    Returns
    -------
    pd.DataFrame
        Pivot table DataFrame.
    """
    return pd.pivot_table(
        df,
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc,
        fill_value=fill_value,
    )


__all__ = ["pivot_df"]
