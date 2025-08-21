import pandas as pd

from pandas_functions.add_suffix_to_df_columns import add_suffix_to_df_columns


def test_add_suffix_to_df_columns() -> None:
    """Adding a suffix should rename all columns."""
    df = pd.DataFrame({"A": [1], "B": [2]})
    expected = pd.DataFrame({"A_suf": [1], "B_suf": [2]})
    result = add_suffix_to_df_columns(df, "_suf")
    pd.testing.assert_frame_equal(result, expected)
