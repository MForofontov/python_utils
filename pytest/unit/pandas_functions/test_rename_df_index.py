import pandas as pd
import pytest

from pandas_functions.rename_df_index import rename_df_index


def test_rename_df_index() -> None:
    """Mapping should rename index labels."""
    df = pd.DataFrame({"A": [1]}, index=["old"])
    expected = pd.DataFrame({"A": [1]}, index=["new"])
    result = rename_df_index(df, {"old": "new"})
    pd.testing.assert_frame_equal(result, expected)


def test_rename_df_index_missing_label() -> None:
    """Missing labels should raise KeyError."""
    df = pd.DataFrame({"A": [1]}, index=["old"])
    with pytest.raises(KeyError):
        rename_df_index(df, {"missing": "new"})
