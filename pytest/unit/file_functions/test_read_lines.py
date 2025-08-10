from pathlib import Path

import pytest

from file_functions.read_lines import read_lines


def test_read_lines_entire_file_with_stripping(tmp_path: Path) -> None:
    """Test reading entire file with default stripping."""
    # Test case 1: Read entire file
    file_path: Path = tmp_path / "input.txt"
    file_path.write_text("  line1  \nline2\n line3 ")
    expected: list[str] = ["line1", "line2", "line3"]
    returned: list[str] = read_lines(str(file_path))
    assert returned == expected, "Should read all lines stripped of whitespace"


def test_read_lines_limited_num_lines(tmp_path: Path) -> None:
    """Test reading only a limited number of lines."""
    # Test case 2: Limit number of lines
    file_path: Path = tmp_path / "input.txt"
    file_path.write_text("line1\nline2\nline3\n")
    returned: list[str] = read_lines(str(file_path), num_lines=2)
    expected: list[str] = ["line1", "line2"]
    assert returned == expected, "Should return the first num_lines lines"


def test_read_lines_strip_false(tmp_path: Path) -> None:
    """Test that setting strip=False preserves whitespace."""
    # Test case 3: Preserve whitespace
    file_path: Path = tmp_path / "input.txt"
    file_path.write_text("  line1  \nline2\n")
    returned: list[str] = read_lines(str(file_path), strip=False)
    expected: list[str] = ["  line1  \n", "line2\n"]
    assert returned == expected, "Should preserve whitespace when strip=False"


def test_read_lines_zero_num_lines(tmp_path: Path) -> None:
    """Test that providing num_lines=0 returns an empty list."""
    # Test case 4: Zero num_lines
    file_path: Path = tmp_path / "input.txt"
    file_path.write_text("line1\nline2\n")
    returned: list[str] = read_lines(str(file_path), num_lines=0)
    expected: list[str] = []
    assert returned == expected, "Should return an empty list when num_lines is 0"


def test_read_lines_negative_num_lines(tmp_path: Path) -> None:
    """Test that providing a negative num_lines returns an empty list."""
    # Test case 5: Negative num_lines
    file_path: Path = tmp_path / "input.txt"
    file_path.write_text("line1\nline2\n")
    returned: list[str] = read_lines(str(file_path), num_lines=-1)
    expected: list[str] = []
    assert returned == expected, "Should return an empty list when num_lines is negative"


def test_read_lines_missing_file(tmp_path: Path) -> None:
    """Test that a missing file raises FileNotFoundError."""
    # Test case 6: Missing file
    missing_file: Path = tmp_path / "missing.txt"
    with pytest.raises(FileNotFoundError):
        read_lines(str(missing_file))
