import pandas as pd
import pytest

from pandas_functions.filter_df_by_column_values import filter_df_by_column_values


def test_filter_df_by_column_values() -> None:
    """Filtering by multiple values should return matching rows."""
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    expected = pd.DataFrame({"A": [1, 3], "B": ["x", "z"]}, index=[0, 2])
    result = filter_df_by_column_values(df, "A", [1, 3])
    pd.testing.assert_frame_equal(result, expected)


def test_filter_df_by_column_values_missing() -> None:
    """Filtering on a non-existent column should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1]})
    with pytest.raises(KeyError):
        filter_df_by_column_values(df, "B", [1])
