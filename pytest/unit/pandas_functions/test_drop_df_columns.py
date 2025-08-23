import pandas as pd
import pytest

from pandas_functions.drop_df_columns import drop_df_columns


def test_drop_df_columns() -> None:
    """
    Dropping specified columns should remove them from the DataFrame.
    """
    # Test case 1: Drop existing column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2], "C": [5, 6]})
    result: pd.DataFrame = drop_df_columns(df, ["B"])
    pd.testing.assert_frame_equal(result, expected)


def test_drop_df_columns_missing() -> None:
    """
    Dropping a non-existent column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        drop_df_columns(df, ["B"])


def test_drop_df_columns_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        drop_df_columns("not a df", ["A"])
