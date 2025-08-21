import pandas as pd
import pandas as pd
import pytest

from pandas_functions.rename_df_columns import rename_df_columns


def test_rename_df_columns() -> None:
    """
    Renaming columns should apply the provided mapping.
    """
    # Test case 1: Rename existing column
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    expected = pd.DataFrame({"X": [1, 2], "B": [3, 4]})
    result = rename_df_columns(df, {"A": "X"})
    pd.testing.assert_frame_equal(result, expected)


def test_rename_df_columns_missing() -> None:
    """
    Renaming a non-existent column should raise ``KeyError``.
    """
    # Test case 2: Missing column
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        rename_df_columns(df, {"B": "X"})


def test_rename_df_columns_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 3: Invalid DataFrame input
    with pytest.raises(AttributeError):
        rename_df_columns("not a df", {"A": "X"})
