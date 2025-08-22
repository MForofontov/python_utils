from pathlib import Path

import pandas as pd
import pytest

from pandas_functions.export_df_to_file import export_df_to_file


def test_export_and_read_back(tmp_path: Path) -> None:
    """
    Export a DataFrame and read it back to verify contents.
    """

    # Test case 1: Export and verify content
    df: pd.DataFrame = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    file_path: Path = tmp_path / "data.csv"
    export_df_to_file(df, file_path)
    result: pd.DataFrame = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(result, df)


def test_unwritable_destination(tmp_path: Path) -> None:
    """
    Writing to an unwritable destination should raise ``OSError``.
    """

    # Test case 2: Attempt to write to directory
    df: pd.DataFrame = pd.DataFrame({"a": [1]})
    directory: Path = tmp_path / "dir"
    directory.mkdir()
    with pytest.raises(OSError):
        export_df_to_file(df, directory)


def test_export_df_to_file_invalid_df(tmp_path: Path) -> None:
    """
    Ensure passing a non-DataFrame raises ``AttributeError``.
    """

    # Test case 3: Invalid DataFrame input
    file_path: Path = tmp_path / "data.csv"
    with pytest.raises(AttributeError):
        export_df_to_file("not a df", file_path)
