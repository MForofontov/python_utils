import pandas as pd
import pytest

from pandas_functions.select_df_columns import select_df_columns


def test_select_df_columns() -> None:
    """Selecting specific columns should return them in order."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    expected = pd.DataFrame({"B": [3, 4], "A": [1, 2]})
    result = select_df_columns(df, ["B", "A"])
    pd.testing.assert_frame_equal(result, expected)


def test_select_df_columns_missing() -> None:
    """Requesting a non-existent column should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        select_df_columns(df, ["B"])

