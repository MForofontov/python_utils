import pandas as pd
import pytest

from pandas_functions.sort_df_by_index import sort_df_by_index


def test_sort_df_by_index_ascending() -> None:
    """
    Sorting by index in ascending order should reorder rows.
    """
    # Test case 1: Sort ascending
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]}, index=[2, 1])
    expected: pd.DataFrame = pd.DataFrame({"A": [2, 1]}, index=[1, 2])
    result: pd.DataFrame = sort_df_by_index(df)
    pd.testing.assert_frame_equal(result, expected)


def test_sort_df_by_index_descending() -> None:
    """
    Sorting by index in descending order should reverse row order.
    """
    # Test case 2: Sort descending
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]}, index=[2, 1])
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2]}, index=[2, 1])
    result: pd.DataFrame = sort_df_by_index(df, ascending=False)
    pd.testing.assert_frame_equal(result, expected)


def test_sort_df_by_index_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        sort_df_by_index("not a df")

