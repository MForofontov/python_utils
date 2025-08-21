import pandas as pd
import pytest

from pandas_functions import concat_dataframes


def test_concat_dataframes():
    df1 = pd.DataFrame({"A": [1, 2]})
    df2 = pd.DataFrame({"A": [3]})
    result = concat_dataframes([df1, df2])
    expected = pd.DataFrame({"A": [1, 2, 3]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_concat_dataframes_type_error():
    df1 = pd.DataFrame({"A": [1]})
    with pytest.raises(TypeError):
        concat_dataframes([df1, "not a df"])


def test_concat_dataframes_empty():
    with pytest.raises(ValueError):
        concat_dataframes([])
