import pandas as pd
import pytest

from pandas_functions.shuffle_df_rows import shuffle_df_rows


def test_shuffle_df_rows() -> None:
    """
    Shuffling rows should change their order deterministically with a seed.
    """
    # Test case 1: Shuffle rows with random_state
    df = pd.DataFrame({"A": [1, 2, 3]})
    expected = pd.DataFrame({"A": [1, 3, 2]})
    result = shuffle_df_rows(df, random_state=1)
    pd.testing.assert_frame_equal(result, expected)


def test_shuffle_df_rows_invalid_df() -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """
    # Test case 2: Invalid DataFrame input
    with pytest.raises(AttributeError):
        shuffle_df_rows("not a df")
