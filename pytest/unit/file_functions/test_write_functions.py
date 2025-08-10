import pytest

from pathlib import Path

import pytest

from file_functions.write_lines import write_lines
from file_functions.write_to_file import write_to_file


def test_write_lines_default_joiner(tmp_path: Path) -> None:
    """Write lines with default newline joiner."""
    # Test case 1: Default joiner
    lines: list[str] = ["one", "two", "three"]
    out_file: Path = tmp_path / "out.txt"
    write_lines(lines, str(out_file))
    assert (
        out_file.read_text() == "one\ntwo\nthree\n"
    ), "Should join lines with newline by default"


def test_write_lines_empty_list(tmp_path: Path) -> None:
    """Writing an empty list results in a file with only a newline."""
    # Test case 2: Empty list
    out_file: Path = tmp_path / "out.txt"
    write_lines([], str(out_file))
    assert out_file.read_text() == "\n", "File should contain only newline"


def test_write_lines_custom_joiner_append(tmp_path: Path) -> None:
    """Use custom joiner and append mode."""
    # Test case 3: Custom joiner with append mode
    out_file: Path = tmp_path / "out.txt"
    write_lines(["start"], str(out_file))
    write_lines(["a", "b"], str(out_file), joiner="|", write_mode="a")
    assert out_file.read_text() == "start\na|b\n", "Should append with custom joiner"


def test_write_to_file_appends_end_char(tmp_path: Path) -> None:
    """`write_to_file` appends the provided end_char."""
    # Test case 4: Append end_char
    out_file: Path = tmp_path / "out.txt"
    write_to_file("hello", str(out_file), "w", "END")
    assert out_file.read_text() == "helloEND", "Should append end_char"


def test_write_lines_unwritable_destination(tmp_path: Path) -> None:
    """Writing to an unwritable destination raises an error."""
    # Test case 5: Unwritable destination
    directory_path: Path = tmp_path / "subdir"
    directory_path.mkdir()
    with pytest.raises(OSError):
        write_lines(["data"], str(directory_path))
