import os
import tempfile

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from pyutils_collection.file_functions import write_to_file


def test_write_to_file_basic_write() -> None:
    """
    Test case 1: Basic file write operation.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Hello, World!"

        # Act
        write_to_file(content, output_file)

        # Assert
        with open(output_file) as f:
            assert f.read() == content


def test_write_to_file_write_mode() -> None:
    """
    Test case 2: Write with explicit write mode.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Test content"

        # Act
        write_to_file(content, output_file, mode="w")

        # Assert
        with open(output_file) as f:
            assert f.read() == content


def test_write_to_file_append_mode() -> None:
    """
    Test case 3: Write in append mode.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")

        # Create initial content
        initial_content = "Initial content"
        with open(output_file, "w") as f:
            f.write(initial_content)

        additional_content = " Additional content"

        # Act
        write_to_file(additional_content, output_file, mode="a")

        # Assert
        with open(output_file) as f:
            assert f.read() == initial_content + additional_content


def test_write_to_file_custom_end_char() -> None:
    """
    Test case 4: Write with custom end character.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Test content"
        end_char = "END"

        # Act
        write_to_file(content, output_file, end_char=end_char)

        # Assert
        with open(output_file) as f:
            assert f.read() == content + end_char


def test_write_to_file_unicode_content() -> None:
    """
    Test case 5: Handle Unicode characters in content.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Hello 世界! ümläuts émojis 🎉"

        # Act
        write_to_file(content, output_file)

        # Assert
        with open(output_file, encoding="utf-8") as f:
            assert f.read() == content


def test_write_to_file_empty_content() -> None:
    """
    Test case 6: Write empty content.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = ""

        # Act
        write_to_file(content, output_file)

        # Assert
        with open(output_file) as f:
            assert f.read() == content


def test_write_to_file_exclusive_mode() -> None:
    """
    Test case 7: Write in exclusive mode (file must not exist).
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file = os.path.join(tmp_dir, "new_file.txt")
        content = "New file content"

        # Act
        write_to_file(content, new_file, mode="x")

        # Assert
        with open(new_file) as f:
            assert f.read() == content


def test_write_to_file_multiline_content() -> None:
    """
    Test case 8: Handle multiline content.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Line 1\nLine 2\nLine 3"

        # Act
        write_to_file(content, output_file)

        # Assert
        with open(output_file) as f:
            assert f.read() == content


def test_write_to_file_special_characters() -> None:
    """
    Test case 9: Handle special characters in content.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "output.txt")
        content = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?`~"

        # Act
        write_to_file(content, output_file)

        # Assert
        with open(output_file) as f:
            assert f.read() == content


def test_write_to_file_type_validation() -> None:
    """
    Test case 10: Type validation for parameters.
    """
    # Test invalid data type
    with pytest.raises(TypeError, match="data must be a string"):
        write_to_file(123, "output.txt")

    # Test invalid file_path type
    with pytest.raises(TypeError, match="file_path must be a string"):
        write_to_file("content", 123)

    # Test invalid mode type
    with pytest.raises(TypeError, match="mode must be a string"):
        write_to_file("content", "output.txt", mode=123)

    # Test invalid end_char type
    with pytest.raises(TypeError, match="end_char must be a string"):
        write_to_file("content", "output.txt", end_char=123)


def test_write_to_file_value_validation() -> None:
    """
    Test case 11: Value validation for parameters.
    """
    # Test empty file_path
    with pytest.raises(ValueError, match="file_path cannot be empty"):
        write_to_file("content", "")

    # Test invalid mode
    with pytest.raises(ValueError, match="mode must be 'w', 'a', or 'x'"):
        write_to_file("content", "output.txt", mode="invalid")


def test_write_to_file_exclusive_mode_file_exists() -> None:
    """
    Test case 12: Exclusive mode should raise error if file exists.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir:
        existing_file = os.path.join(tmp_dir, "existing.txt")

        # Create existing file
        with open(existing_file, "w") as f:
            f.write("existing content")

        # Act & Assert
        with pytest.raises(FileExistsError):
            write_to_file("new content", existing_file, mode="x")
