import pandas as pd
import pytest

from pandas_functions.df_to_dict import df_to_dict


def test_df_to_dict_default() -> None:
    """DataFrame should convert to nested dict with default orientation."""
    df: pd.DataFrame = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    expected: dict = {"col1": {0: 1, 1: 2}, "col2": {0: 3, 1: 4}}
    assert df_to_dict(df) == expected


def test_df_to_dict_list_orient() -> None:
    """DataFrame should convert to list-oriented dictionary."""
    df: pd.DataFrame = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    expected: dict = {"col1": [1, 2], "col2": [3, 4]}
    assert df_to_dict(df, orient="list") == expected


def test_df_to_dict_invalid_input() -> None:
    """Passing a non-DataFrame should raise a TypeError."""
    with pytest.raises(TypeError):
        df_to_dict({"col1": [1, 2]})
