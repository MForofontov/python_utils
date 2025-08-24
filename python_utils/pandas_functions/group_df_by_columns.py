import pandas as pd
from collections.abc import Iterable, Mapping, Callable


def group_df_by_columns(
    df: pd.DataFrame,
    group_cols: str | Iterable[str],
    agg: Mapping[str, Callable | str | Iterable[Callable | str]],
) -> pd.DataFrame:
    """Group a DataFrame by the specified columns and aggregate.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to group.
    group_cols : str or Iterable[str]
        Column name(s) to group by.
    agg : Mapping[str, Callable | str | Iterable[Callable | str]]
        Aggregation instructions passed to ``DataFrame.groupby().agg``.

    Returns
    -------
    pd.DataFrame
        Aggregated DataFrame with the group columns as regular columns.
    """
    return df.groupby(group_cols).agg(agg).reset_index()


__all__ = ["group_df_by_columns"]
