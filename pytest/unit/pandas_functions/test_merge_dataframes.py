import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pandas_functions.merge_dataframes import merge_dataframes


def test_merge_dataframes_inner() -> None:
    """
    Verify inner merge returns intersection of keys.
    """
    # Test case 1: Inner merge on common key
    df1: pd.DataFrame = pd.DataFrame({"id": [1, 2], "value1": ["a", "b"]})
    df2: pd.DataFrame = pd.DataFrame({"id": [2, 3], "value2": ["x", "y"]})
    expected: pd.DataFrame = pd.DataFrame(
        {"id": [2], "value1": ["b"], "value2": ["x"]})

    result = merge_dataframes(df1, df2, on="id", how="inner")
    assert_frame_equal(result, expected)


def test_merge_dataframes_outer() -> None:
    """
    Verify outer merge includes all keys from both DataFrames.
    """
    # Test case 2: Outer merge
    df1: pd.DataFrame = pd.DataFrame({"id": [1, 2], "value1": ["a", "b"]})
    df2: pd.DataFrame = pd.DataFrame({"id": [2, 3], "value2": ["x", "y"]})
    expected: pd.DataFrame = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "value1": ["a", "b", np.nan],
            "value2": [np.nan, "x", "y"],
        }
    )

    result = merge_dataframes(df1, df2, on="id", how="outer")
    assert_frame_equal(result, expected)


def test_merge_dataframes_missing_on() -> None:
    """
    Missing join column should raise ``KeyError``.
    """
    # Test case 3: Missing join column
    df1: pd.DataFrame = pd.DataFrame({"id": [1]})
    df2: pd.DataFrame = pd.DataFrame({"other": [1]})
    with pytest.raises(KeyError):
        merge_dataframes(df1, df2, on="id")


def test_merge_dataframes_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 4: Invalid DataFrame input
    with pytest.raises(AttributeError):
        merge_dataframes("not a df", pd.DataFrame({"id": [1]}), on="id")
