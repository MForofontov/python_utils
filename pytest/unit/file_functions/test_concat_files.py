import pytest
from file_functions.concat_files import concat_files


def test_concat_files_appends_two_files(tmp_path) -> None:
    """Test that concatenating two source files appends both contents in order."""
    src1 = tmp_path / "src1.txt"
    src1.write_text("Hello\n")
    src2 = tmp_path / "src2.txt"
    src2.write_text("World")
    dest = tmp_path / "dest.txt"

    concat_files(str(src1), str(dest))
    concat_files(str(src2), str(dest))

    assert dest.read_text() == "Hello\nWorld", "Destination should contain combined contents"


def test_concat_files_empty_source(tmp_path) -> None:
    """Test that concatenating an empty source file leaves destination unchanged."""
    dest = tmp_path / "dest.txt"
    dest.write_text("Existing content")
    empty = tmp_path / "empty.txt"
    empty.write_text("")

    concat_files(str(empty), str(dest))

    assert dest.read_text() == "Existing content", "Destination should remain unchanged"


def test_concat_files_missing_source(tmp_path) -> None:
    """Test that providing a missing source file raises FileNotFoundError."""
    dest = tmp_path / "dest.txt"
    dest.write_text("data")

    with pytest.raises(FileNotFoundError):
        concat_files(str(tmp_path / "missing.txt"), str(dest))
