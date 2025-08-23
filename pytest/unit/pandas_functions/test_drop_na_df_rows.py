import pandas as pd
import pytest

from pandas_functions.drop_na_df_rows import drop_na_df_rows


def test_drop_na_df_rows_subset() -> None:
    """
    Rows with NA in specified subset should be dropped.
    """
    # Test case 1: Drop NA based on subset
    df: pd.DataFrame = pd.DataFrame({"A": [1, None, 2], "B": [4, 5, None]})
    result: pd.DataFrame = drop_na_df_rows(df, ["A"])
    expected: pd.DataFrame = pd.DataFrame({"A": [1.0, 2.0], "B": [4.0, None]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_na_df_rows_all_columns() -> None:
    """
    Rows with NA in any column should be dropped when no subset is provided.
    """
    # Test case 2: Drop NA from all columns
    df: pd.DataFrame = pd.DataFrame({"A": [1, None], "B": [4, 5]})
    result: pd.DataFrame = drop_na_df_rows(df)
    expected: pd.DataFrame = pd.DataFrame({"A": [1.0], "B": [4]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_na_df_rows_missing_column() -> None:
    """
    Requesting a missing column should raise ``KeyError``.
    """
    # Test case 3: Missing column
    df: pd.DataFrame = pd.DataFrame({"A": [1, None]})
    with pytest.raises(KeyError):
        drop_na_df_rows(df, ["B"])


def test_drop_na_df_rows_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 4: Invalid DataFrame input
    with pytest.raises(AttributeError):
        drop_na_df_rows(123, ["A"])
