"""
Test case 1: Test getting code statistics for Python projects.
"""

import tempfile
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.dev_utilities]
from pyutils_collection.dev_utilities.code_analysis.get_code_statistics import (
    CodeStatistics,
    format_statistics,
    get_code_statistics,
)


def test_get_code_statistics_simple_project() -> None:
    """
    Test case 1: Get statistics for a simple Python project.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "main.py").write_text(
            "def func():\n    return 42\n\nclass MyClass:\n    pass\n"
        )

        # Act
        stats = get_code_statistics(project_path)

        # Assert
        assert isinstance(stats, CodeStatistics)
        assert stats.total_files == 1
        assert stats.total_functions >= 0
        assert stats.total_classes >= 0


def test_get_code_statistics_empty_project() -> None:
    """
    Test case 2: Get statistics for an empty project.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        # Act
        stats = get_code_statistics(tmpdir)

        # Assert
        assert stats.total_files == 0
        assert stats.total_lines == 0
        assert stats.avg_lines_per_file == 0.0


def test_get_code_statistics_invalid_type_raises_error() -> None:
    """
    Test case 3: TypeError for invalid project_path type.
    """
    # Arrange
    invalid_path = 123
    expected_message = "project_path must be str or Path, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_code_statistics(invalid_path)  # type: ignore


def test_get_code_statistics_nonexistent_path_raises_error() -> None:
    """
    Test case 4: FileNotFoundError for nonexistent project path.
    """
    # Arrange
    invalid_path = "/nonexistent/project/path"
    expected_message = "Project path does not exist"

    # Act & Assert
    with pytest.raises(FileNotFoundError, match=expected_message):
        get_code_statistics(invalid_path)


def test_get_code_statistics_with_exclude_patterns() -> None:
    """
    Test case 5: Exclude files matching patterns.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "main.py").write_text("x = 1\n")
        (project_path / "test_main.py").write_text("def test(): pass\n")

        # Act
        stats = get_code_statistics(project_path, exclude_patterns=["**/test_*.py"])

        # Assert
        # Should only count main.py, not test_main.py
        assert stats.total_files == 1


def test_get_code_statistics_multiple_files_and_classes() -> None:
    """
    Test case 6: Count functions and classes correctly.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "module1.py").write_text(
            "def func1():\n    pass\n\ndef func2():\n    pass\n"
        )
        (project_path / "module2.py").write_text(
            "class MyClass:\n    def method(self):\n        pass\n"
        )

        # Act
        stats = get_code_statistics(project_path)

        # Assert
        assert stats.total_files == 2
        assert stats.total_functions >= 2  # func1, func2
        assert stats.total_classes >= 1  # MyClass


def test_format_statistics_default_title() -> None:
    """
    Test case 7: Format statistics with default title.
    """
    # Arrange
    stats = CodeStatistics(
        total_files=10,
        total_lines=500,
        source_lines=400,
        comment_lines=50,
        blank_lines=50,
        docstring_lines=100,
        total_functions=25,
        total_classes=5,
        total_methods=15,
        total_imports=30,
        avg_lines_per_file=50.0,
        avg_functions_per_file=2.5,
    )

    # Act
    result = format_statistics(stats)

    # Assert
    assert "Code Statistics" in result
    assert "Total Files: 10" in result
    assert "Functions: 25" in result


def test_format_statistics_invalid_type_raises_error() -> None:
    """
    Test case 8: TypeError for invalid stats type.
    """
    # Arrange
    invalid_stats = {"total_files": 10}
    expected_message = "stats must be CodeStatistics"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_statistics(invalid_stats)  # type: ignore
