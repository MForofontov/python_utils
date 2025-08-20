import pandas as pd

from pandas_functions.drop_na_df_columns import drop_na_df_columns


def test_drop_na_df_columns_any() -> None:
    """Columns with any NA values should be dropped by default."""
    df = pd.DataFrame({"A": [1, 2], "B": [None, None], "C": [1, None]})
    result = drop_na_df_columns(df)
    expected = pd.DataFrame({"A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_drop_na_df_columns_all() -> None:
    """Using ``how='all'`` should only drop columns with all NA values."""
    df = pd.DataFrame({"A": [1, 2], "B": [None, None], "C": [1, None]})
    result = drop_na_df_columns(df, how="all")
    expected = pd.DataFrame({"A": [1, 2], "C": [1, None]})
    pd.testing.assert_frame_equal(result, expected)
