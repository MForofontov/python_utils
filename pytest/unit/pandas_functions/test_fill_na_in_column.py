import numpy as np
import pandas as pd
import pytest

from pandas_functions.fill_na_in_column import fill_na_in_column


def test_fill_na_in_column() -> None:
    """
    NaN values in the specified column should be replaced.
    """
    # Test case 1: Fill NaNs in column
    df: pd.DataFrame = pd.DataFrame({"A": [1, np.nan, 3]})
    expected: pd.DataFrame = pd.DataFrame({"A": [1.0, 0.0, 3.0]})
    result: pd.DataFrame = fill_na_in_column(df, "A", 0)
    pd.testing.assert_frame_equal(result, expected)


def test_fill_na_in_column_missing_column() -> None:
    """
    Passing an invalid column name should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        fill_na_in_column(df, "B", 0)


def test_fill_na_in_column_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        fill_na_in_column("not a df", "A", 0)
