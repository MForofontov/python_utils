from pathlib import Path

import pytest
from file_functions import tsv_to_dict


def test_tsv_to_dict_basic(tmp_path: Path) -> None:
    """
    Test case 1: Basic TSV conversion with default separator.
    """
    content: str = "a\t1\t2\nb\t3\t4\n"
    file: Path = tmp_path / "sample.tsv"
    file.write_text(content)
    result: dict[str, list[str]] = tsv_to_dict(str(file))
    assert result == {
        "a": ["1", "2"],
        "b": ["3", "4"],
    }, "Should parse TSV into dictionary"


def test_tsv_to_dict_skip_header(tmp_path: Path) -> None:
    """
    Test case 2: Ensure the header line is skipped when skip_header=True.
    """
    content: str = "h1\th2\nk1\tv1\n"
    file: Path = tmp_path / "sample.tsv"
    file.write_text(content)
    result: dict[str, list[str]] = tsv_to_dict(str(file), skip_header=True)
    assert result == {"k1": ["v1"]}, "Header line should be skipped"


def test_tsv_to_dict_non_tab_separator(tmp_path: Path) -> None:
    """
    Test case 3: Support arbitrary separators when converting.
    """
    content: str = "a,1,2\nb,3,4\n"
    file: Path = tmp_path / "sample.csv"
    file.write_text(content)
    result: dict[str, list[str]] = tsv_to_dict(str(file), sep=",")
    assert result == {
        "a": ["1", "2"],
        "b": ["3", "4"],
    }, "Should handle custom separators"


def test_tsv_to_dict_duplicate_keys(tmp_path: Path) -> None:
    """
    Test case 4: Later entries should overwrite earlier ones for duplicate keys.
    """
    content: str = "a\t1\nb\t2\na\t3\n"
    file: Path = tmp_path / "dup.tsv"
    file.write_text(content)
    result: dict[str, list[str]] = tsv_to_dict(str(file))
    assert result == {"a": ["3"], "b": ["2"]}, "Later key should overwrite"


def test_empty_tsv_file_returns_empty_dict(tmp_path: Path) -> None:
    """
    Test case 5: Empty TSV file should return an empty dictionary.
    """
    file: Path = tmp_path / "empty.tsv"
    file.write_text("")
    result: dict[str, list[str]] = tsv_to_dict(str(file))
    assert result == {}, "Empty file should return empty dict"


def test_missing_file_path_raises_FileNotFoundError(tmp_path: Path) -> None:
    """
    Test case 6: A nonexistent file path should raise FileNotFoundError.
    """
    missing_file: Path = tmp_path / "does_not_exist.tsv"
    with pytest.raises(FileNotFoundError):
        tsv_to_dict(str(missing_file))
