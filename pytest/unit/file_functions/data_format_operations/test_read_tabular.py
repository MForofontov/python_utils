from pathlib import Path

import pytest

from file_functions import read_tabular


def test_read_tabular_standard_tsv(tmp_path: Path) -> None:
    """
    Test case 1: Test reading a standard TSV file.
    """
    content: str = "col1\tcol2\n1\t2\n"
    file_path: Path = tmp_path / "test.tsv"
    file_path.write_text(content)
    expected: list[list[str]] = [["col1", "col2"], ["1", "2"]]
    assert read_tabular(str(file_path)) == expected, "Should read TSV data"


def test_read_tabular_custom_delimiter(tmp_path: Path) -> None:
    """
    Test case 2: Test reading a file with a custom delimiter.
    """
    content: str = "a,b\n3,4\n"
    file_path: Path = tmp_path / "test.csv"
    file_path.write_text(content)
    expected: list[list[str]] = [["a", "b"], ["3", "4"]]
    assert (
        read_tabular(str(file_path), delimiter=",") == expected
    ), "Should parse CSV with custom delimiter"


def test_read_tabular_empty_file(tmp_path: Path) -> None:
    """
    Test case 3: Test reading an empty file returns an empty list.
    """
    file_path: Path = tmp_path / "empty.tsv"
    file_path.write_text("")
    assert read_tabular(str(file_path)) == [], "Empty file should return empty list"


def test_read_tabular_missing_file(tmp_path: Path) -> None:
    """
    Test case 4: Test missing file raises FileNotFoundError.
    """
    missing_file: Path = tmp_path / "missing.tsv"
    with pytest.raises(FileNotFoundError):
        read_tabular(str(missing_file))
