from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from python_utils.file_functions import write_lines, write_to_file


def test_write_lines_default_joiner(tmp_path: Path) -> None:
    """
    Test case 1: Write lines with default newline joiner.
    """
    lines: list[str] = ["one", "two", "three"]
    out_file: Path = tmp_path / "out.txt"
    write_lines(lines, str(out_file))
    assert out_file.read_text() == "one\ntwo\nthree\n", (
        "Should join lines with newline by default"
    )


def test_write_lines_empty_list(tmp_path: Path) -> None:
    """
    Test case 2: Writing an empty list results in a file with only a newline.
    """
    out_file: Path = tmp_path / "out.txt"
    write_lines([], str(out_file))
    assert out_file.read_text() == "\n", "File should contain only newline"


def test_write_lines_custom_joiner_append(tmp_path: Path) -> None:
    """
    Test case 3: Use custom joiner and append mode.
    """
    out_file: Path = tmp_path / "out.txt"
    write_lines(["start"], str(out_file))
    write_lines(["a", "b"], str(out_file), joiner="|", write_mode="a")
    assert out_file.read_text() == "start\na|b\n", "Should append with custom joiner"


def test_write_to_file_appends_end_char(tmp_path: Path) -> None:
    """
    Test case 4: `write_to_file` appends the provided end_char.
    """
    out_file: Path = tmp_path / "out.txt"
    write_to_file("hello", str(out_file), "w", "END")
    assert out_file.read_text() == "helloEND", "Should append end_char"


def test_write_lines_unwritable_destination(tmp_path: Path) -> None:
    """
    Test case 5: Writing to an unwritable destination raises an error.
    """
    directory_path: Path = tmp_path / "subdir"
    directory_path.mkdir()
    with pytest.raises(OSError):
        write_lines(["data"], str(directory_path))
