import pandas as pd
import pytest

from pandas_functions.sort_df_by_index import sort_df_by_index


def test_sort_df_by_index() -> None:
    """
    Sorting by index should reorder rows accordingly.
    """
    # Test case 1: Sort ascending
    df = pd.DataFrame({"A": [1, 2]}, index=[2, 1])
    expected_asc = pd.DataFrame({"A": [2, 1]}, index=[1, 2])
    result_asc = sort_df_by_index(df)
    pd.testing.assert_frame_equal(result_asc, expected_asc)

    # Test case 2: Sort descending
    expected_desc = pd.DataFrame({"A": [1, 2]}, index=[2, 1])
    result_desc = sort_df_by_index(df, ascending=False)
    pd.testing.assert_frame_equal(result_desc, expected_desc)


def test_sort_df_by_index_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        sort_df_by_index("not a df")
