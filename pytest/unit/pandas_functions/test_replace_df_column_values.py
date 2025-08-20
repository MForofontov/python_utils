import pandas as pd
import pytest

from pandas_functions.replace_df_column_values import replace_df_column_values


def test_replace_df_column_values() -> None:
    """Values in a column should be replaced using the mapping."""
    df = pd.DataFrame({"A": [1, 2, 1]})
    expected = pd.DataFrame({"A": ["one", "two", "one"]})
    result = replace_df_column_values(df, "A", {1: "one", 2: "two"})
    pd.testing.assert_frame_equal(result, expected)


def test_replace_df_column_values_missing_column() -> None:
    """Replacing a non-existent column should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1]})
    with pytest.raises(KeyError):
        replace_df_column_values(df, "B", {1: "one"})
