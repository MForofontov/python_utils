from pathlib import Path

import pandas as pd
import pytest

from pandas_functions.import_df_from_file import import_df_from_file


def test_import_df_from_file_basic(tmp_path: Path) -> None:
    """Import a CSV file into a DataFrame."""
    # Test case 1: Basic CSV import
    df: pd.DataFrame = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    file_path: Path = tmp_path / "data.csv"
    df.to_csv(file_path, index=False)
    result: pd.DataFrame = import_df_from_file(file_path)
    pd.testing.assert_frame_equal(result, df)


def test_import_df_from_file_custom_sep(tmp_path: Path) -> None:
    """Import a file using a custom separator."""
    # Test case 2: Custom separator
    df: pd.DataFrame = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    file_path: Path = tmp_path / "data.tsv"
    df.to_csv(file_path, index=False, sep="\t")
    result: pd.DataFrame = import_df_from_file(file_path, sep="\t")
    pd.testing.assert_frame_equal(result, df)


def test_import_df_from_file_errors(tmp_path: Path) -> None:
    """Missing file or invalid content should raise appropriate errors."""
    # Test case 3: Missing file
    missing_file: Path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        import_df_from_file(missing_file)

    # Test case 4: Invalid content
    invalid_file: Path = tmp_path / "invalid.csv"
    invalid_file.write_text("")
    with pytest.raises(ValueError):
        import_df_from_file(invalid_file)
