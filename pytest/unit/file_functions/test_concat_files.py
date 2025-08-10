from pathlib import Path

import pytest

from file_functions.concat_files import concat_files


def test_concat_files_appends_two_files(tmp_path: Path) -> None:
    """Test that concatenating two source files appends both contents in order."""
    # Test case 1: Append contents of two files
    src1: Path = tmp_path / "src1.txt"
    src1.write_text("Hello\n")
    src2: Path = tmp_path / "src2.txt"
    src2.write_text("World")
    dest: Path = tmp_path / "dest.txt"

    concat_files(str(src1), str(dest))
    concat_files(str(src2), str(dest))

    assert dest.read_text() == "Hello\nWorld", "Destination should contain combined contents"


def test_concat_files_empty_source(tmp_path: Path) -> None:
    """Test that concatenating an empty source file leaves destination unchanged."""
    # Test case 2: Empty source file
    dest: Path = tmp_path / "dest.txt"
    dest.write_text("Existing content")
    empty: Path = tmp_path / "empty.txt"
    empty.write_text("")

    concat_files(str(empty), str(dest))

    assert dest.read_text() == "Existing content", "Destination should remain unchanged"


def test_concat_files_missing_source(tmp_path: Path) -> None:
    """Test that providing a missing source file raises FileNotFoundError."""
    # Test case 3: Missing source file
    dest: Path = tmp_path / "dest.txt"
    dest.write_text("data")

    with pytest.raises(FileNotFoundError):
        concat_files(str(tmp_path / "missing.txt"), str(dest))
