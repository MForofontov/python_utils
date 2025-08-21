import pandas as pd
import pytest

from pandas_functions.sort_df_columns import sort_df_columns


def test_sort_df_columns_ascending() -> None:
    """
    Columns should be sorted alphabetically.
    """
    # Test case 1: Sort columns ascending
    df = pd.DataFrame({"B": [1], "A": [2]})
    result = sort_df_columns(df)
    expected = pd.DataFrame({"A": [2], "B": [1]})
    pd.testing.assert_frame_equal(result, expected)


def test_sort_df_columns_descending() -> None:
    """
    Descending order should reverse column order.
    """
    # Test case 2: Sort columns descending
    df = pd.DataFrame({"B": [1], "A": [2]})
    result = sort_df_columns(df, ascending=False)
    expected = pd.DataFrame({"B": [1], "A": [2]})
    pd.testing.assert_frame_equal(result, expected)


def test_sort_df_columns_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        sort_df_columns("not a df")
