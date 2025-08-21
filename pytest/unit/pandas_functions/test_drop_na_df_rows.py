import pandas as pd
import pytest

from pandas_functions import drop_na_df_rows


def test_drop_na_df_rows_subset():
    df = pd.DataFrame({"A": [1, None, 2], "B": [4, 5, None]})
    result = drop_na_df_rows(df, ["A"])
    expected = pd.DataFrame({"A": [1.0, 2.0], "B": [4.0, None]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_na_df_rows_all_columns():
    df = pd.DataFrame({"A": [1, None], "B": [4, 5]})
    result = drop_na_df_rows(df)
    expected = pd.DataFrame({"A": [1.0], "B": [4]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_na_df_rows_missing_column():
    df = pd.DataFrame({"A": [1, None]})
    with pytest.raises(KeyError):
        drop_na_df_rows(df, ["B"])
