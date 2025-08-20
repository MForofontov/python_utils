import pandas as pd
import pytest

from pandas_functions import apply_function_to_column


def test_apply_function_to_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = apply_function_to_column(df, "A", lambda x: x * 2)
    expected = pd.DataFrame({"A": [2, 4, 6]})
    pd.testing.assert_frame_equal(result, expected)


def test_apply_function_to_column_missing():
    df = pd.DataFrame({"A": [1]})
    with pytest.raises(KeyError):
        apply_function_to_column(df, "B", lambda x: x)
