import pandas as pd
import pytest

from pandas_functions.group_df_by_columns import group_df_by_columns


def test_group_df_by_columns() -> None:
    """
    Grouping by a column and aggregating should compute expected values.
    """
    # Test case 1: Group and aggregate
    df: pd.DataFrame = pd.DataFrame({"A": ["x", "x", "y"], "B": [1, 2, 3], "C": [4, 5, 6]})
    expected: pd.DataFrame = pd.DataFrame({"A": ["x", "y"], "B": [1.5, 3.0], "C": [9, 6]})
    result: pd.DataFrame = group_df_by_columns(df, "A", {"B": "mean", "C": "sum"})
    pd.testing.assert_frame_equal(result, expected)


def test_group_df_by_columns_missing_column() -> None:
    """
    Grouping by a missing column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        group_df_by_columns(df, "C", {"B": "sum"})


def test_group_df_by_columns_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        group_df_by_columns("not a df", "A", {"B": "sum"})
