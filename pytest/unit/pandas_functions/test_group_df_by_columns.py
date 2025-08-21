import pandas as pd
import pytest

from pandas_functions import group_df_by_columns


def test_group_df_by_columns():
    df = pd.DataFrame({"A": ["x", "x", "y"], "B": [1, 2, 3], "C": [4, 5, 6]})
    expected = pd.DataFrame({"A": ["x", "y"], "B": [1.5, 3.0], "C": [9, 6]})
    result = group_df_by_columns(df, "A", {"B": "mean", "C": "sum"})
    pd.testing.assert_frame_equal(result, expected)


def test_group_df_by_columns_missing_column():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        group_df_by_columns(df, "C", {"B": "sum"})
