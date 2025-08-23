import pandas as pd
import pytest

from pandas_functions.drop_na_df_columns import drop_na_df_columns


def test_drop_na_df_columns_any() -> None:
    """
    Columns with any NA values should be dropped by default.
    """
    # Test case 1: Drop columns with any NA
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [None, None], "C": [1, None]})
    result: pd.DataFrame = drop_na_df_columns(df)
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_drop_na_df_columns_all() -> None:
    """
    Using ``how='all'`` should only drop columns with all NA values.
    """
    # Test case 2: Drop columns with all NA
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [None, None], "C": [1, None]})
    result: pd.DataFrame = drop_na_df_columns(df, how="all")
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2], "C": [1, None]})
    pd.testing.assert_frame_equal(result, expected)


def test_drop_na_df_columns_invalid_how() -> None:
    """
    Invalid ``how`` value should raise ``ValueError``.
    """
    # Test case 3: Invalid how parameter
    df: pd.DataFrame = pd.DataFrame({"A": [1]})
    with pytest.raises(ValueError):
        drop_na_df_columns(df, how="invalid")
