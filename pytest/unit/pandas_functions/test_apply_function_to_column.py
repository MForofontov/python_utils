import pandas as pd
import pytest

from pandas_functions.apply_function_to_column import apply_function_to_column


def test_apply_function_to_column() -> None:
    """
    Test applying a function to a DataFrame column.
    """
    # Test case 1: Apply lambda to column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2, 3]})
    result: pd.DataFrame = apply_function_to_column(df, "A", lambda x: x * 2)
    expected: pd.DataFrame = pd.DataFrame({"A": [2, 4, 6]})
    pd.testing.assert_frame_equal(result, expected)


def test_apply_function_to_column_missing() -> None:
    """
    Ensure missing column raises ``KeyError``.
    """
    # Test case 2: Missing column
    df: pd.DataFrame = pd.DataFrame({"A": [1]})
    with pytest.raises(KeyError):
        apply_function_to_column(df, "B", lambda x: x)


def test_apply_function_to_column_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        apply_function_to_column("not a df", "A", lambda x: x)
