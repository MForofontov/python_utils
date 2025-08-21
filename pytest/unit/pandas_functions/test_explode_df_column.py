import pandas as pd
import pytest

from pandas_functions.explode_df_column import explode_df_column


def test_explode_df_column_basic() -> None:
    df = pd.DataFrame({"id": [1, 2], "tags": [["a", "b"], ["c"]]})
    result = explode_df_column(df, "tags")
    expected = pd.DataFrame({"id": [1, 1, 2], "tags": ["a", "b", "c"]})
    pd.testing.assert_frame_equal(result, expected)


def test_explode_df_column_missing_column() -> None:
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(KeyError):
        explode_df_column(df, "missing")
