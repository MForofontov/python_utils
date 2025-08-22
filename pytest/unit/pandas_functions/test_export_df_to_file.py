from pathlib import Path

import pandas as pd
import pytest

from pandas_functions.export_df_to_file import export_df_to_file


def test_export_and_read_back(tmp_path: Path) -> None:
    """Export a DataFrame and read it back to verify contents."""
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    file_path = tmp_path / "data.csv"
    export_df_to_file(df, file_path)
    result = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df, result)


def test_unwritable_destination(tmp_path: Path) -> None:
    """Writing to an unwritable destination raises an error."""
    df = pd.DataFrame({"a": [1]})
    directory = tmp_path / "dir"
    directory.mkdir()
    with pytest.raises(OSError):
        export_df_to_file(df, directory)
