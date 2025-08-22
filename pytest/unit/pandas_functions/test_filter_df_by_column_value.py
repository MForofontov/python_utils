import pandas as pd
import pytest

from pandas_functions.filter_df_by_column_value import filter_df_by_column_value


def test_filter_df_by_column_value() -> None:
    """
    Filtering by a column value should return matching rows.
    """
    # Test case 1: Filter rows by value
    df = pd.DataFrame({"A": [1, 2, 1], "B": ["x", "y", "z"]})
    expected = pd.DataFrame({"A": [1, 1], "B": ["x", "z"]})
    result = filter_df_by_column_value(df, "A", 1)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_filter_df_by_column_value_missing_column() -> None:
    """
    Filtering with a missing column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pytest.raises(KeyError):
        filter_df_by_column_value(df, "B", 1)


def test_filter_df_by_column_value_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        filter_df_by_column_value("not a df", "A", 1)
