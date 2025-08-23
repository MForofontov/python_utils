import pandas as pd
import pytest

from pandas_functions.reset_df_index import reset_df_index


def test_reset_df_index() -> None:
    """
    Resetting the index should move it to a column by default.
    """
    # Test case 1: Reset index with column insertion
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]}, index=["x", "y"])
    result: pd.DataFrame = reset_df_index(df)
    expected: pd.DataFrame = pd.DataFrame({"index": ["x", "y"], "A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_reset_df_index_drop() -> None:
    """
    Dropping the index should remove it from the DataFrame.
    """
    # Test case 2: Reset index with drop
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]}, index=[10, 11])
    result: pd.DataFrame = reset_df_index(df, drop=True)
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_reset_df_index_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        reset_df_index("not a df")
