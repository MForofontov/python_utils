import pandas as pd
import pytest

from pandas_functions.drop_df_columns import drop_df_columns


def test_drop_df_columns() -> None:
    """Dropping specified columns should remove them from the DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    expected = pd.DataFrame({"A": [1, 2], "C": [5, 6]})
    result = drop_df_columns(df, ["B"])
    pd.testing.assert_frame_equal(result, expected)


def test_drop_df_columns_missing() -> None:
    """Dropping a non-existent column should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        drop_df_columns(df, ["B"])
