import pandas as pd


def replace_df_column_values(
    df: pd.DataFrame, column: str, value_map: dict[object, object]
) -> pd.DataFrame:
    """Replace values in ``column`` of ``df`` using ``value_map``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column to modify.
    column : str
        Name of the column whose values will be replaced.
    value_map : dict[object, object]
        Mapping from existing values to new values.

    Returns
    -------
    pd.DataFrame
        DataFrame with updated column values.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(column)
    result = df.copy()
    result[column] = result[column].replace(value_map)
    return result


__all__ = ["replace_df_column_values"]
