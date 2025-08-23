import pandas as pd
import pytest

from pandas_functions.add_prefix_to_df_columns import add_prefix_to_df_columns


def test_add_prefix_to_df_columns() -> None:
    """
    Test adding a prefix to DataFrame columns.
    """
    # Test case 1: Adds prefix to each column
    df: pd.DataFrame = pd.DataFrame({"A": [1], "B": [2]})
    expected: pd.DataFrame = pd.DataFrame({"pre_A": [1], "pre_B": [2]})
    result: pd.DataFrame = add_prefix_to_df_columns(df, "pre_")
    pd.testing.assert_frame_equal(result, expected)


def test_add_prefix_to_df_columns_invalid_input() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 2: Invalid DataFrame input
    with pytest.raises(AttributeError):
        add_prefix_to_df_columns("not a df", "pre_")
