import pandas as pd
import pytest

from pandas_functions.pivot_df import pivot_df


def test_pivot_df() -> None:
    """
    Pivoting a DataFrame should reorganize data correctly.
    """
    # Test case 1: Pivot with aggregation and fill value
    df: pd.DataFrame = pd.DataFrame({"A": [1, 1, 2], "B": ["x", "y", "x"], "C": [10, 20, 30]})
    expected: pd.DataFrame = pd.DataFrame({"x": [10, 30], "y": [20, 0]}, index=pd.Index([1, 2], name="A"))
    expected.columns.name = "B"
    result: pd.DataFrame = pivot_df(df, index="A", columns="B", values="C", aggfunc="sum", fill_value=0)
    pd.testing.assert_frame_equal(result, expected)


def test_pivot_df_missing_column() -> None:
    """
    Passing a missing column should raise ``KeyError``.
    """
    # Test case 2: Missing values column
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        pivot_df(df, index="A", columns="B", values="C")


def test_pivot_df_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``TypeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(TypeError):
        pivot_df(123, index="A", columns="B", values="C")
