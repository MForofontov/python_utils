import pandas as pd
import pytest

from pandas_functions.convert_df_column_dtype import convert_df_column_dtype


def test_convert_df_column_dtype() -> None:
    """Converting a column should change its dtype."""
    df = pd.DataFrame({"A": ["1", "2"]})
    result = convert_df_column_dtype(df, "A", int)
    expected = pd.DataFrame({"A": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_convert_df_column_dtype_missing() -> None:
    """Requesting a missing column should raise ``KeyError``."""
    df = pd.DataFrame({"A": [1]})
    with pytest.raises(KeyError):
        convert_df_column_dtype(df, "B", int)
