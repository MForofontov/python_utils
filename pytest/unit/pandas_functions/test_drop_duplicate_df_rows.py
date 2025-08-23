import pandas as pd
import pytest

from pandas_functions.drop_duplicate_df_rows import drop_duplicate_df_rows


def test_drop_duplicate_df_rows() -> None:
    """
    Duplicate rows should be removed.
    """
    # Test case 1: Drop duplicate rows
    df: pd.DataFrame = pd.DataFrame({"A": [1, 1, 2], "B": [3, 3, 4]})
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    result: pd.DataFrame = drop_duplicate_df_rows(df)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_duplicate_df_rows_invalid_keep() -> None:
    """
    Invalid ``keep`` value should raise ``ValueError``.
    """
    # Test case 2: Invalid keep parameter
    df: pd.DataFrame = pd.DataFrame({"A": [1, 1]})
    with pytest.raises(ValueError):
        drop_duplicate_df_rows(df, keep="invalid")


def test_drop_duplicate_df_rows_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        drop_duplicate_df_rows("not a df")
