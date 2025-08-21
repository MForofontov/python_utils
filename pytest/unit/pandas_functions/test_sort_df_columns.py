import pandas as pd

from pandas_functions.sort_df_columns import sort_df_columns


def test_sort_df_columns_ascending() -> None:
    """Columns should be sorted alphabetically."""
    df = pd.DataFrame({"B": [1], "A": [2]})
    result = sort_df_columns(df)
    expected = pd.DataFrame({"A": [2], "B": [1]})
    pd.testing.assert_frame_equal(result, expected)


def test_sort_df_columns_descending() -> None:
    """Descending order should reverse column order."""
    df = pd.DataFrame({"B": [1], "A": [2]})
    result = sort_df_columns(df, ascending=False)
    expected = pd.DataFrame({"B": [1], "A": [2]})
    pd.testing.assert_frame_equal(result, expected)
