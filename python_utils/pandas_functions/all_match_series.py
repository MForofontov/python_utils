import pandas as pd


def all_match_series(series1: pd.Series, series2: pd.Series) -> bool:
    """Check if all elements of ``series1`` are contained in ``series2``.

    Parameters
    ----------
    series1 : pd.Series
        The query Series whose elements are checked for presence in ``series2``.
    series2 : pd.Series
        The reference Series against which ``series1`` is compared.

    Returns
    -------
    bool
        ``True`` if all elements of ``series1`` are found in ``series2``; ``False`` otherwise.

    Raises
    ------
    TypeError
        If ``series1`` or ``series2`` is not a pandas Series or contains elements that
        cannot be compared (e.g., unhashable elements).
    """
    if not isinstance(series1, pd.Series):
        raise TypeError("series1 must be a pandas Series")
    if not isinstance(series2, pd.Series):
        raise TypeError("series2 must be a pandas Series")

    try:
        # ``Series.isin`` checks membership element-wise
        return bool(series1.isin(series2).all())
    except TypeError as exc:
        raise TypeError(f"An element in the series cannot be compared: {exc}")


__all__ = ["all_match_series"]
