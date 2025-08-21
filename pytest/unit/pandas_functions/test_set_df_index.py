import pandas as pd
import pytest

from pandas_functions.set_df_index import set_df_index


def test_set_df_index() -> None:
    """Setting a column as index should remove it by default."""
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    result = set_df_index(df, ["B"])
    expected = pd.DataFrame({"A": [1, 2]}, index=pd.Index(["x", "y"], name="B"))
    pd.testing.assert_frame_equal(result, expected)


def test_set_df_index_drop_false() -> None:
    """Setting the index with ``drop=False`` should retain the column."""
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    result = set_df_index(df, ["B"], drop=False)
    expected = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]}).set_index("B", drop=False)
    pd.testing.assert_frame_equal(result, expected)


def test_set_df_index_missing() -> None:
    """Setting a non-existent column as index should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        set_df_index(df, ["B"])
