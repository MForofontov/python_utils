import pandas as pd
import pytest

from pandas_functions.dict_to_df import dict_to_df


def test_dict_to_df_basic() -> None:
    """Convert a dictionary with list values to a DataFrame."""
    # Test case 1: Dictionary with list values
    data: dict[str, list[int]] = {"A": [1, 2], "B": [3, 4]}
    expected: pd.DataFrame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    result: pd.DataFrame = dict_to_df(data)
    pd.testing.assert_frame_equal(result, expected)


def test_dict_to_df_nested() -> None:
    """Convert a nested dictionary to a DataFrame."""
    # Test case 2: Nested dictionary input
    data: dict[str, dict[str, int]] = {
        "col1": {"row1": 1, "row2": 2},
        "col2": {"row1": 3},
    }
    expected: pd.DataFrame = pd.DataFrame({
        "col1": {"row1": 1, "row2": 2},
        "col2": {"row1": 3},
    })
    result: pd.DataFrame = dict_to_df(data)
    pd.testing.assert_frame_equal(result, expected)


def test_dict_to_df_invalid_input() -> None:
    """Passing a non-dictionary should raise ``ValueError``."""
    # Test case 3: Invalid dictionary input
    with pytest.raises(ValueError):
        dict_to_df("not a dict")  # type: ignore[arg-type]
