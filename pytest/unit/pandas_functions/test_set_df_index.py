import pandas as pd
import pytest

from pandas_functions.set_df_index import set_df_index


def test_set_df_index() -> None:
    """
    Setting a column as index should remove it by default.
    """
    # Test case 1: Set column as index with drop
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    result = set_df_index(df, ["B"])
    expected = pd.DataFrame({"A": [1, 2]}, index=pd.Index(["x", "y"], name="B"))
    pd.testing.assert_frame_equal(result, expected)


def test_set_df_index_drop_false() -> None:
    """
    Setting the index with ``drop=False`` should retain the column.
    """
    # Test case 2: Set index without dropping column
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    result = set_df_index(df, ["B"], drop=False)
    expected = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]}).set_index("B", drop=False)
    pd.testing.assert_frame_equal(result, expected)


def test_set_df_index_missing() -> None:
    """
    Setting a non-existent column as index should raise ``KeyError``.
    """
    # Test case 3: Missing column
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(KeyError):
        set_df_index(df, ["B"])


def test_set_df_index_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 4: Invalid DataFrame input
    with pytest.raises(AttributeError):
        set_df_index("not a df", ["A"])
