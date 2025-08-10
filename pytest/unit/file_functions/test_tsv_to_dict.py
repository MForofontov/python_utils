import pytest
from file_functions.tsv_to_dict import tsv_to_dict


def test_tsv_to_dict_basic(tmp_path) -> None:
    """Basic TSV conversion with default separator."""
    content = "a\t1\t2\nb\t3\t4\n"
    file = tmp_path / "sample.tsv"
    file.write_text(content)
    result = tsv_to_dict(str(file))
    assert result == {"a": ["1", "2"], "b": ["3", "4"]}


def test_tsv_to_dict_skip_header(tmp_path) -> None:
    """Ensure the header line is skipped when skip_header=True."""
    content = "h1\th2\nk1\tv1\n"
    file = tmp_path / "sample.tsv"
    file.write_text(content)
    result = tsv_to_dict(str(file), skip_header=True)
    assert result == {"k1": ["v1"]}


def test_tsv_to_dict_non_tab_separator(tmp_path) -> None:
    """Support arbitrary separators when converting."""
    content = "a,1,2\nb,3,4\n"
    file = tmp_path / "sample.csv"
    file.write_text(content)
    result = tsv_to_dict(str(file), sep=",")
    assert result == {"a": ["1", "2"], "b": ["3", "4"]}


def test_tsv_to_dict_duplicate_keys(tmp_path) -> None:
    """Later entries should overwrite earlier ones for duplicate keys."""
    content = "a\t1\nb\t2\na\t3\n"
    file = tmp_path / "dup.tsv"
    file.write_text(content)
    result = tsv_to_dict(str(file))
    assert result == {"a": ["3"], "b": ["2"]}


def test_empty_tsv_file_returns_empty_dict(tmp_path) -> None:
    """Empty TSV file should return an empty dictionary."""
    file = tmp_path / "empty.tsv"
    file.write_text("")
    result = tsv_to_dict(str(file))
    assert result == {}


def test_missing_file_path_raises_FileNotFoundError(tmp_path) -> None:
    """A nonexistent file path should raise FileNotFoundError."""
    missing_file = tmp_path / "does_not_exist.tsv"
    with pytest.raises(FileNotFoundError):
        tsv_to_dict(str(missing_file))
