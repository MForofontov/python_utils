import pandas as pd
import pytest

from pandas_functions import pivot_df


def test_pivot_df():
    df = pd.DataFrame({"A": [1, 1, 2], "B": ["x", "y", "x"], "C": [10, 20, 30]})
    expected = pd.DataFrame(
        {"x": [10, 30], "y": [20, 0]}, index=pd.Index([1, 2], name="A")
    )
    expected.columns.name = "B"
    result = pivot_df(df, index="A", columns="B", values="C", aggfunc="sum", fill_value=0)
    pd.testing.assert_frame_equal(result, expected)


def test_pivot_df_missing_column():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        pivot_df(df, index="A", columns="B", values="C")
