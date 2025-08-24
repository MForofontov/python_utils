import pandas as pd


def df_to_dict(df: pd.DataFrame, orient: str = "dict") -> dict:
    """
    Convert a pandas DataFrame to a dictionary using ``DataFrame.to_dict``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to convert.
    orient : str, optional
        Orientation of the resulting dictionary, by default ``"dict"``.

    Returns
    -------
    dict
        Dictionary representation of the DataFrame.

    Raises
    ------
    TypeError
        If ``df`` is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    return df.to_dict(orient=orient)


__all__ = ["df_to_dict"]
