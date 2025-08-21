import pandas as pd
import pytest

from pandas_functions.split_df_column import split_df_column


def test_split_df_column_basic() -> None:
    """
    Splitting a column into multiple columns should distribute values.
    """
    # Test case 1: Basic split by space
    df = pd.DataFrame({"name": ["John Doe", "Jane Smith"], "age": [30, 25]})
    result = split_df_column(df, "name", ["first", "last"], " ")
    expected = pd.DataFrame({"age": [30, 25], "first": ["John", "Jane"], "last": ["Doe", "Smith"]})
    pd.testing.assert_frame_equal(result, expected)


def test_split_df_column_missing_column() -> None:
    """
    Splitting a non-existent column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df = pd.DataFrame({"name": ["John Doe"]})
    with pytest.raises(KeyError):
        split_df_column(df, "missing", ["first", "last"], " ")


def test_split_df_column_mismatch_into() -> None:
    """
    Providing mismatched target columns should raise ``ValueError``.
    """
    # Test case 3: Mismatched target columns
    df = pd.DataFrame({"name": ["John Doe"], "age": [30]})
    with pytest.raises(ValueError):
        split_df_column(df, "name", ["first", "middle", "last"], " ")


def test_split_df_column_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 4: Invalid DataFrame input
    with pytest.raises(AttributeError):
        split_df_column("not a df", "name", ["first", "last"], " ")
