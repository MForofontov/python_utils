import pandas as pd
import pytest

from pandas_functions.explode_df_column import explode_df_column


def test_explode_df_column_basic() -> None:
    """
    Exploding a column with lists should create multiple rows.
    """
    # Test case 1: Basic explosion
    df = pd.DataFrame({"id": [1, 2], "tags": [["a", "b"], ["c"]]})
    result = explode_df_column(df, "tags")
    expected = pd.DataFrame({"id": [1, 1, 2], "tags": ["a", "b", "c"]})
    pd.testing.assert_frame_equal(result, expected)


def test_explode_df_column_missing_column() -> None:
    """
    Requesting a missing column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(KeyError):
        explode_df_column(df, "missing")


def test_explode_df_column_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        explode_df_column("not a df", "tags")
