import pytest

from file_functions.write_lines import write_lines
from file_functions.write_to_file import write_to_file


def test_write_lines_default_joiner(tmp_path) -> None:
    """Write lines with default newline joiner."""
    lines = ["one", "two", "three"]
    out_file = tmp_path / "out.txt"
    write_lines(lines, str(out_file))
    assert out_file.read_text() == "one\ntwo\nthree\n"


def test_write_lines_empty_list(tmp_path) -> None:
    """Writing an empty list results in a file with only a newline."""
    out_file = tmp_path / "out.txt"
    write_lines([], str(out_file))
    assert out_file.read_text() == "\n"


def test_write_lines_custom_joiner_append(tmp_path) -> None:
    """Use custom joiner and append mode."""
    out_file = tmp_path / "out.txt"
    write_lines(["start"], str(out_file))
    write_lines(["a", "b"], str(out_file), joiner="|", write_mode="a")
    assert out_file.read_text() == "start\na|b\n"


def test_write_to_file_appends_end_char(tmp_path) -> None:
    """`write_to_file` appends the provided end_char."""
    out_file = tmp_path / "out.txt"
    write_to_file("hello", str(out_file), "w", "END")
    assert out_file.read_text() == "helloEND"


def test_write_lines_unwritable_destination(tmp_path) -> None:
    """Writing to an unwritable destination raises an error."""
    directory_path = tmp_path / "subdir"
    directory_path.mkdir()
    with pytest.raises(OSError):
        write_lines(["data"], str(directory_path))
