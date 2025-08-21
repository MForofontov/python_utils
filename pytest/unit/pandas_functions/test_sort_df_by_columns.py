import pandas as pd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pandas_functions.sort_df_by_columns import sort_df_by_columns


def test_sort_df_by_single_column() -> None:
    """
    Sorting by a single column should order values ascending.
    """
    # Test case 1: Sort by one column
    df = pd.DataFrame({"A": [3, 1, 2]})
    expected = pd.DataFrame({"A": [1, 2, 3]})
    result = sort_df_by_columns(df, "A")
    assert_frame_equal(result.reset_index(drop=True), expected)


def test_sort_df_by_multiple_columns_descending() -> None:
    """
    Sorting by multiple columns with mixed order should work.
    """
    # Test case 2: Sort by multiple columns
    df = pd.DataFrame({"A": [1, 2, 1], "B": [2, 1, 1]})
    expected = pd.DataFrame({"A": [1, 1, 2], "B": [2, 1, 1]})
    result = sort_df_by_columns(df, ["A", "B"], ascending=[True, False])
    assert_frame_equal(result.reset_index(drop=True), expected)


def test_sort_df_by_columns_missing() -> None:
    """
    Sorting by a non-existent column should raise ``KeyError``.
    """
    # Test case 3: Missing column
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        sort_df_by_columns(df, "B")


def test_sort_df_by_columns_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 4: Invalid DataFrame input
    with pytest.raises(AttributeError):
        sort_df_by_columns("not a df", "A")

