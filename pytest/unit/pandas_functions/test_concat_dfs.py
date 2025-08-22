import pandas as pd
import pytest

from pandas_functions import concat_dfs


def test_concat_dfs_rows() -> None:
    """
    Concatenating DataFrames along rows should combine them vertically.
    """
    # Test case 1: Concatenate along rows
    df1: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2: pd.DataFrame = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
    result: pd.DataFrame = concat_dfs([df1, df2])
    expected: pd.DataFrame = pd.DataFrame(
        {"A": [1, 2, 5, 6], "B": [3, 4, 7, 8]}, index=[0, 1, 0, 1]
    )
    assert result.shape == (4, 2)
    assert list(result.columns) == ["A", "B"]
    pd.testing.assert_frame_equal(result, expected)


def test_concat_dfs_columns() -> None:
    """
    Concatenating DataFrames along columns should combine them horizontally.
    """
    # Test case 2: Concatenate along columns
    df1: pd.DataFrame = pd.DataFrame({"A": [1, 2]})
    df2: pd.DataFrame = pd.DataFrame({"B": [3, 4]})
    result: pd.DataFrame = concat_dfs([df1, df2], axis=1)
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    assert result.shape == (2, 2)
    assert list(result.columns) == ["A", "B"]
    pd.testing.assert_frame_equal(result, expected)


def test_concat_dfs_invalid_item() -> None:
    """
    Passing a non-DataFrame in the sequence should raise ``TypeError``.
    """
    # Test case 3: Non-DataFrame element
    df1: pd.DataFrame = pd.DataFrame({"A": [1]})
    with pytest.raises(TypeError):
        concat_dfs([df1, "not a df"])


def test_concat_dfs_empty_sequence() -> None:
    """
    An empty sequence should raise ``ValueError``.
    """
    # Test case 4: Empty sequence
    with pytest.raises(ValueError):
        concat_dfs([])
