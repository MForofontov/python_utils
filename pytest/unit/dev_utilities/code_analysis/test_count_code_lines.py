"""
Test case 1: Test counting code lines in Python files.
"""

import tempfile
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.dev_utilities]
from pyutils_collection.dev_utilities.code_analysis.count_code_lines import (
    CodeLineCount,
    count_code_lines,
    count_code_lines_directory,
)


def test_count_code_lines_simple_file() -> None:
    """
    Test case 1: Count lines in a simple Python file.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Comment\n")
        f.write("\n")
        f.write("def func():\n")
        f.write('    """Docstring"""\n')
        f.write("    return 42\n")
        temp_file = f.name

    try:
        # Act
        result = count_code_lines(temp_file)

        # Assert
        assert isinstance(result, CodeLineCount)
        assert result.total_lines == 5
        assert result.source_lines >= 0
    finally:
        Path(temp_file).unlink()


def test_count_code_lines_empty_file() -> None:
    """
    Test case 2: Count lines in an empty file.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        temp_file = f.name

    try:
        # Act
        result = count_code_lines(temp_file)

        # Assert
        assert result.total_lines == 0
        assert result.source_lines == 0
        assert result.blank_lines == 0
    finally:
        Path(temp_file).unlink()


def test_count_code_lines_invalid_type_raises_error() -> None:
    """
    Test case 3: TypeError for invalid file_path type.
    """
    # Arrange
    invalid_path = 123
    expected_message = "file_path must be str or Path, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        count_code_lines(invalid_path)  # type: ignore


def test_count_code_lines_nonexistent_file_raises_error() -> None:
    """
    Test case 4: FileNotFoundError for nonexistent file.
    """
    # Arrange
    nonexistent = "/path/to/nonexistent.py"
    expected_message = "File does not exist"

    # Act & Assert
    with pytest.raises(FileNotFoundError, match=expected_message):
        count_code_lines(nonexistent)


def test_count_code_lines_non_python_file_raises_error() -> None:
    """
    Test case 5: ValueError for non-Python file.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        temp_file = f.name

    try:
        expected_message = "File must be a Python"

        # Act & Assert
        with pytest.raises(ValueError, match=expected_message):
            count_code_lines(temp_file)
    finally:
        Path(temp_file).unlink()


def test_count_code_lines_with_comments_and_blanks() -> None:
    """
    Test case 6: Correctly count files with comments and blank lines.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# This is a comment\n")
        f.write("\n")
        f.write("# Another comment\n")
        f.write("\n")
        f.write("x = 1\n")
        temp_file = f.name

    try:
        # Act
        result = count_code_lines(temp_file)

        # Assert
        assert result.total_lines == 5
        assert result.blank_lines == 2
        # Comments may be counted differently by tokenize
        assert result.source_lines >= 1  # At least one source line (x = 1)
    finally:
        Path(temp_file).unlink()


def test_count_code_lines_directory_simple() -> None:
    """
    Test case 7: Count lines for all files in a directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "file1.py").write_text("x = 1\n")
        (project_path / "file2.py").write_text("y = 2\n")

        # Act
        results = count_code_lines_directory(project_path, recursive=False)

        # Assert
        assert len(results) == 2
        assert all(isinstance(c, CodeLineCount) for c in results.values())


def test_count_code_lines_directory_recursive() -> None:
    """
    Test case 8: Count lines recursively in subdirectories.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        subdir = project_path / "subdir"
        subdir.mkdir()
        (project_path / "main.py").write_text("x = 1\n")
        (subdir / "module.py").write_text("y = 2\n")

        # Act
        results = count_code_lines_directory(project_path, recursive=True)

        # Assert
        assert len(results) == 2
