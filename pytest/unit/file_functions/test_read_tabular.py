import pytest
from file_functions.read_tabular import read_tabular


def test_read_tabular_standard_tsv(tmp_path) -> None:
    """Test reading a standard TSV file."""
    content: str = "col1\tcol2\n1\t2\n"
    file_path = tmp_path / "test.tsv"
    file_path.write_text(content)
    expected: list[list[str]] = [["col1", "col2"], ["1", "2"]]
    assert read_tabular(str(file_path)) == expected


def test_read_tabular_custom_delimiter(tmp_path) -> None:
    """Test reading a file with a custom delimiter."""
    content: str = "a,b\n3,4\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(content)
    expected: list[list[str]] = [["a", "b"], ["3", "4"]]
    assert read_tabular(str(file_path), delimiter=",") == expected


def test_read_tabular_empty_file(tmp_path) -> None:
    """Test reading an empty file returns an empty list."""
    file_path = tmp_path / "empty.tsv"
    file_path.write_text("")
    assert read_tabular(str(file_path)) == []


def test_read_tabular_missing_file(tmp_path) -> None:
    """Test missing file raises FileNotFoundError."""
    missing_file = tmp_path / "missing.tsv"
    with pytest.raises(FileNotFoundError):
        read_tabular(str(missing_file))
