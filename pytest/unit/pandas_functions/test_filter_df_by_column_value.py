import pandas as pd
import pytest

from pandas_functions import filter_df_by_column_value


def test_filter_df_by_column_value():
    df = pd.DataFrame({"A": [1, 2, 1], "B": ["x", "y", "z"]})
    expected = pd.DataFrame({"A": [1, 1], "B": ["x", "z"]})
    result = filter_df_by_column_value(df, "A", 1)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_filter_df_by_column_value_missing_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pytest.raises(KeyError):
        filter_df_by_column_value(df, "B", 1)
