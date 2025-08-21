import pandas as pd
import pytest

from pandas_functions import melt_df


def test_melt_df():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    expected = pd.DataFrame(
        {"A": [1, 2, 1, 2], "variable": ["B", "B", "C", "C"], "value": [3, 4, 5, 6]}
    )
    result = melt_df(df, id_vars="A", value_vars=["B", "C"], var_name="variable", value_name="value")
    pd.testing.assert_frame_equal(result, expected)


def test_melt_df_missing_column():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(KeyError):
        melt_df(df, id_vars="A", value_vars=["B", "C"])
