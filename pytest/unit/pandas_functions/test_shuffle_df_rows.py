import pandas as pd

from pandas_functions.shuffle_df_rows import shuffle_df_rows


def test_shuffle_df_rows() -> None:
    """Shuffling rows should change their order deterministically with a seed."""
    df = pd.DataFrame({"A": [1, 2, 3]})
    expected = pd.DataFrame({"A": [1, 3, 2]})
    result = shuffle_df_rows(df, random_state=1)
    pd.testing.assert_frame_equal(result, expected)
