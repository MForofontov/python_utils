import os
import tempfile

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from pyutils_collection.file_functions import write_lines


def test_write_lines_default_joiner() -> None:
    """
    Test case 1: Write lines with default newline joiner.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = ["line1", "line2", "line3"]

        # Act
        write_lines(lines, output_file)

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "line1\nline2\nline3\n"


def test_write_lines_custom_joiner() -> None:
    """
    Test case 2: Write lines with custom joiner.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = ["apple", "banana", "cherry"]

        # Act
        write_lines(lines, output_file, joiner=", ")

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "apple, banana, cherry\n"


def test_write_lines_append_mode() -> None:
    """
    Test case 3: Write lines in append mode.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")

        # Create initial content
        with open(output_file, "w") as f:
            f.write("initial\n")

        lines = ["appended1", "appended2"]

        # Act
        write_lines(lines, output_file, write_mode="a")

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "initial\nappended1\nappended2\n"


def test_write_lines_empty_list() -> None:
    """
    Test case 4: Write empty list of lines.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = []

        # Act
        write_lines(lines, output_file)

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "\n"  # Just the final newline


def test_write_lines_lines_with_non_strings() -> None:
    """
    Test case 5: Handle non-string items in lines list.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = ["string", 123, True, None]

        # Act
        write_lines(lines, output_file)

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "string\n123\nTrue\nNone\n"


def test_write_lines_unicode_content() -> None:
    """
    Test case 6: Handle Unicode characters in lines.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = ["Hello 世界", "ümläuts", "émojis 🎉"]

        # Act
        write_lines(lines, output_file)

        # Assert
        with open(output_file, encoding="utf-8") as f:
            content = f.read()
        assert content == "Hello 世界\nümläuts\némojis 🎉\n"


def test_write_lines_overwrite_mode() -> None:
    """
    Test case 7: Write lines in overwrite mode (default).
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")

        # Create initial content
        with open(output_file, "w") as f:
            f.write("old content\n")

        lines = ["new", "content"]

        # Act
        write_lines(lines, output_file)

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "new\ncontent\n"


def test_write_lines_custom_joiner_no_spaces() -> None:
    """
    Test case 8: Write lines with custom joiner without spaces.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        lines = ["a", "b", "c", "d"]

        # Act
        write_lines(lines, output_file, joiner="|")

        # Assert
        with open(output_file) as f:
            content = f.read()
        assert content == "a|b|c|d\n"


def test_write_lines_type_validation() -> None:
    """
    Test case 9: Type validation for parameters.
    """
    # Test invalid lines type
    with pytest.raises(TypeError, match="lines must be a list"):
        write_lines("not_a_list", "output.txt")

    # Test invalid file_path type
    with pytest.raises(TypeError, match="file_path must be a string"):
        write_lines(["line1"], 123)

    # Test invalid joiner type
    with pytest.raises(TypeError, match="joiner must be a string"):
        write_lines(["line1"], "output.txt", joiner=123)

    # Test invalid write_mode type
    with pytest.raises(TypeError, match="write_mode must be a string"):
        write_lines(["line1"], "output.txt", write_mode=123)


def test_write_lines_value_validation() -> None:
    """
    Test case 10: Value validation for parameters.
    """
    # Test empty file_path
    with pytest.raises(ValueError, match="file_path cannot be empty"):
        write_lines(["line1"], "")

    # Test invalid write_mode
    with pytest.raises(ValueError, match="write_mode must be 'w' or 'a'"):
        write_lines(["line1"], "output.txt", write_mode="invalid")
