import pandas as pd
import pytest

from pandas_functions.melt_df import melt_df


def test_melt_df() -> None:
    """
    Melting a DataFrame should convert columns into rows.
    """
    # Test case 1: Melt DataFrame with id and value vars
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    expected: pd.DataFrame = pd.DataFrame(
        {"A": [1, 2, 1, 2], "variable": ["B", "B", "C", "C"], "value": [3, 4, 5, 6]}
    )
    result: pd.DataFrame = melt_df(df, id_vars="A", value_vars=["B", "C"], var_name="variable", value_name="value")
    pd.testing.assert_frame_equal(result, expected)


def test_melt_df_missing_column() -> None:
    """
    Passing missing ``value_vars`` should raise ``KeyError``.
    """
    # Test case 2: Missing value column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        melt_df(df, id_vars="A", value_vars=["B", "C"])


def test_melt_df_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        melt_df("not a df", id_vars="A", value_vars=["B"])
