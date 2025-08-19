from pathlib import Path

import pytest

from pandas_functions.import_df_from_file import import_df_from_file


def test_import_df_from_file_file_not_found(tmp_path: Path) -> None:
    """Ensure a missing file raises FileNotFoundError."""
    missing_file: Path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError, match="File not found"):
        import_df_from_file(missing_file)


def test_import_df_from_file_empty_file(tmp_path: Path) -> None:
    """Ensure an empty file raises ValueError."""
    empty_file: Path = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(ValueError, match="Could not parse"):
        import_df_from_file(empty_file)


def test_import_df_from_file_invalid_kwargs(tmp_path: Path) -> None:
    """Invalid kwargs should propagate to pandas.read_csv and raise ValueError."""
    file_path: Path = tmp_path / "data.csv"
    file_path.write_text("a,b\n1,2\n")
    with pytest.raises(ValueError, match="Could not parse"):
        import_df_from_file(file_path, engine="invalid")
