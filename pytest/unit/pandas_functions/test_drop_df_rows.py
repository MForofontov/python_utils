import pandas as pd
import pytest

from pandas_functions.drop_df_rows import drop_df_rows


def test_drop_df_rows() -> None:
    """Dropping by index labels should remove those rows."""
    df = pd.DataFrame({"A": [1, 2]}, index=["x", "y"])
    result = drop_df_rows(df, ["x"])
    expected = pd.DataFrame({"A": [2]}, index=["y"])
    pd.testing.assert_frame_equal(result, expected)


def test_drop_df_rows_missing_index() -> None:
    """Dropping a non-existent index should raise KeyError."""
    df = pd.DataFrame({"A": [1]}, index=["x"])
    with pytest.raises(KeyError):
        drop_df_rows(df, ["y"])
