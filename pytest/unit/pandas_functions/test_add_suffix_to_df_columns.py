import pandas as pd
import pytest

from pandas_functions.add_suffix_to_df_columns import add_suffix_to_df_columns


def test_add_suffix_to_df_columns() -> None:
    """
    Test adding a suffix to DataFrame columns.
    """
    # Test case 1: Adds suffix to each column
    df: pd.DataFrame = pd.DataFrame({"A": [1], "B": [2]})
    expected: pd.DataFrame = pd.DataFrame({"A_suf": [1], "B_suf": [2]})
    result: pd.DataFrame = add_suffix_to_df_columns(df, "_suf")
    pd.testing.assert_frame_equal(result, expected)


def test_add_suffix_to_df_columns_invalid_input() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 2: Invalid DataFrame input
    with pytest.raises(AttributeError):
        add_suffix_to_df_columns("not a df", "_suf")
