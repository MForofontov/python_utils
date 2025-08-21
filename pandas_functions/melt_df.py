import pandas as pd
from collections.abc import Iterable


def melt_df(
    df: pd.DataFrame,
    id_vars: str | Iterable[str] | None = None,
    value_vars: str | Iterable[str] | None = None,
    var_name: str | None = None,
    value_name: str = "value",
    ignore_index: bool = True,
) -> pd.DataFrame:
    """Unpivot a DataFrame from wide to long format.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to melt.
    id_vars : str or Iterable[str], optional
        Column(s) to use as identifier variables.
    value_vars : str or Iterable[str], optional
        Column(s) to unpivot. If ``None``, use all columns that are not id_vars.
    var_name : str, optional
        Name to use for the variable column.
    value_name : str, optional
        Name to use for the value column, by default ``"value"``.
    ignore_index : bool, optional
        If ``True``, original index is ignored, by default ``True``.

    Returns
    -------
    pd.DataFrame
        Melted DataFrame.
    """
    return pd.melt(
        df,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name=var_name,
        value_name=value_name,
        ignore_index=ignore_index,
    )


__all__ = ["melt_df"]
