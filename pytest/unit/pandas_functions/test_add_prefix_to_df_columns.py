import pandas as pd

from pandas_functions.add_prefix_to_df_columns import add_prefix_to_df_columns


def test_add_prefix_to_df_columns() -> None:
    """Adding a prefix should rename all columns."""
    df = pd.DataFrame({"A": [1], "B": [2]})
    expected = pd.DataFrame({"pre_A": [1], "pre_B": [2]})
    result = add_prefix_to_df_columns(df, "pre_")
    pd.testing.assert_frame_equal(result, expected)
