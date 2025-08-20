import pandas as pd

from pandas_functions.reset_df_index import reset_df_index


def test_reset_df_index() -> None:
    """Resetting the index should move it to a column by default."""
    df = pd.DataFrame({"A": [1, 2]}, index=["x", "y"])
    result = reset_df_index(df)
    expected = pd.DataFrame({"index": ["x", "y"], "A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_reset_df_index_drop() -> None:
    """Dropping the index should remove it from the DataFrame."""
    df = pd.DataFrame({"A": [1, 2]}, index=[10, 11])
    result = reset_df_index(df, drop=True)
    expected = pd.DataFrame({"A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)
