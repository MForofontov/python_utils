"""Tests for find_missing_tests module."""

from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.dev_utilities]
from dev_utilities.project_validation.find_missing_tests import (
    CoverageReport,
    MissingTest,
    find_missing_tests,
    format_coverage_report,
)


def test_find_missing_tests_valid_project(tmp_path: Path) -> None:
    """
    Test finding missing tests in a valid project structure.
    """
    # Arrange - Create project structure
    source_dir = tmp_path / "my_functions"
    source_dir.mkdir()
    (source_dir / "__init__.py").touch()
    (source_dir / "func1.py").touch()
    (source_dir / "func2.py").touch()

    test_dir = tmp_path / "pytest" / "unit" / "my_functions"
    test_dir.mkdir(parents=True)
    (test_dir / "test_func1.py").touch()
    # func2.py has no test

    # Act
    report = find_missing_tests(tmp_path, source_dirs=["my_functions"])

    # Assert
    assert isinstance(report, CoverageReport)
    assert report.total_source_files == 2  # func1, func2 (excluding __init__)
    assert report.files_with_tests == 1
    assert len(report.missing_tests) == 1
    assert report.missing_tests[0].source_file == "my_functions/func2.py"
    assert report.coverage_percentage == 50.0


def test_find_missing_tests_auto_detect_directories(tmp_path: Path) -> None:
    """
    Test auto-detection of source directories.
    """
    # Arrange
    (tmp_path / "string_functions").mkdir()
    (tmp_path / "string_functions" / "utils.py").touch()
    (tmp_path / "math_functions").mkdir()
    (tmp_path / "math_functions" / "calc.py").touch()

    # Act
    report = find_missing_tests(tmp_path)

    # Assert
    assert report.total_source_files == 2
    assert len(report.missing_tests) == 2


def test_find_missing_tests_nested_structure(tmp_path: Path) -> None:
    """
    Test handling of nested directory structures.
    """
    # Arrange
    nested_dir = tmp_path / "data_functions" / "submodule"
    nested_dir.mkdir(parents=True)
    (nested_dir / "processor.py").touch()

    test_dir = tmp_path / "pytest" / "unit" / "data_functions" / "submodule"
    test_dir.mkdir(parents=True)
    (test_dir / "test_processor.py").touch()

    # Act
    report = find_missing_tests(tmp_path, source_dirs=["data_functions"])

    # Assert
    assert report.files_with_tests == 1
    assert len(report.missing_tests) == 0
    assert report.coverage_percentage == 100.0


def test_find_missing_tests_include_init_files(tmp_path: Path) -> None:
    """
    Test including __init__.py files in analysis.
    """
    # Arrange
    source_dir = tmp_path / "utils_functions"
    source_dir.mkdir()
    (source_dir / "__init__.py").touch()
    (source_dir / "helper.py").touch()

    # Act
    report = find_missing_tests(
        tmp_path, source_dirs=["utils_functions"], exclude_init=False
    )

    # Assert
    assert report.total_source_files == 2  # __init__ + helper


def test_find_missing_tests_empty_directory(tmp_path: Path) -> None:
    """
    Test handling of empty source directory.
    """
    # Arrange
    source_dir = tmp_path / "empty_functions"
    source_dir.mkdir()

    # Act
    report = find_missing_tests(tmp_path, source_dirs=["empty_functions"])

    # Assert
    assert report.total_source_files == 0
    assert report.coverage_percentage == 0.0
    assert len(report.missing_tests) == 0


def test_find_missing_tests_custom_test_base_dir(tmp_path: Path) -> None:
    """
    Test using custom test base directory.
    """
    # Arrange
    source_dir = tmp_path / "core_functions"
    source_dir.mkdir()
    (source_dir / "logic.py").touch()

    test_dir = tmp_path / "tests" / "core_functions"
    test_dir.mkdir(parents=True)
    (test_dir / "test_logic.py").touch()

    # Act
    report = find_missing_tests(
        tmp_path, source_dirs=["core_functions"], test_base_dir="tests"
    )

    # Assert
    assert report.files_with_tests == 1
    assert report.coverage_percentage == 100.0


def test_find_missing_tests_invalid_project_path_type_raises_error() -> None:
    """
    Test TypeError for invalid project_path type.
    """
    # Arrange
    invalid_path = 123
    expected_message = "project_path must be str or Path, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_tests(invalid_path)


def test_find_missing_tests_nonexistent_path_raises_error(tmp_path: Path) -> None:
    """
    Test FileNotFoundError for non-existent project path.
    """
    # Arrange
    nonexistent = tmp_path / "does_not_exist"

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Project path does not exist"):
        find_missing_tests(nonexistent)


def test_find_missing_tests_path_is_file_raises_error(tmp_path: Path) -> None:
    """
    Test ValueError when project_path is a file instead of directory.
    """
    # Arrange
    file_path = tmp_path / "file.txt"
    file_path.touch()

    # Act & Assert
    with pytest.raises(ValueError, match="Project path must be a directory"):
        find_missing_tests(file_path)


def test_find_missing_tests_invalid_source_dirs_type_raises_error(
    tmp_path: Path,
) -> None:
    """
    Test TypeError for invalid source_dirs type.
    """
    # Arrange
    invalid_dirs = "not_a_list"
    expected_message = "source_dirs must be list or None, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_tests(tmp_path, source_dirs=invalid_dirs)


def test_find_missing_tests_invalid_test_base_dir_type_raises_error(
    tmp_path: Path,
) -> None:
    """
    Test TypeError for invalid test_base_dir type.
    """
    # Arrange
    invalid_dir = 123
    expected_message = "test_base_dir must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_tests(tmp_path, test_base_dir=invalid_dir)


def test_find_missing_tests_invalid_exclude_init_type_raises_error(
    tmp_path: Path,
) -> None:
    """
    Test TypeError for invalid exclude_init type.
    """
    # Arrange
    invalid_exclude = "yes"
    expected_message = "exclude_init must be bool, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_tests(tmp_path, exclude_init=invalid_exclude)


def test_missing_test_named_tuple_structure() -> None:
    """
    Test MissingTest NamedTuple structure and attributes.
    """
    # Arrange & Act
    missing = MissingTest(
        source_file="src/utils.py",
        expected_test_file="tests/test_utils.py",
        module="src",
    )

    # Assert
    assert missing.source_file == "src/utils.py"
    assert missing.expected_test_file == "tests/test_utils.py"
    assert missing.module == "src"
    assert isinstance(missing, tuple)


def test_test_coverage_report_named_tuple_structure() -> None:
    """
    Test CoverageReport NamedTuple structure and attributes.
    """
    # Arrange
    missing = MissingTest("src/a.py", "tests/test_a.py", "src")

    # Act
    report = CoverageReport(
        total_source_files=10,
        files_with_tests=8,
        missing_tests=[missing],
        coverage_percentage=80.0,
    )

    # Assert
    assert report.total_source_files == 10
    assert report.files_with_tests == 8
    assert len(report.missing_tests) == 1
    assert report.coverage_percentage == 80.0
    assert isinstance(report, tuple)


def test_format_coverage_report_basic_output() -> None:
    """
    Test basic formatting of coverage report.
    """
    # Arrange
    missing = MissingTest(
        source_file="utils/helper.py",
        expected_test_file="tests/utils/test_helper.py",
        module="utils",
    )
    report = CoverageReport(
        total_source_files=5,
        files_with_tests=4,
        missing_tests=[missing],
        coverage_percentage=80.0,
    )

    # Act
    output = format_coverage_report(report, verbose=False)

    # Assert
    assert "Total Source Files: 5" in output
    assert "Files with Tests: 4" in output
    assert "Missing Tests: 1" in output
    assert "Coverage: 80.0%" in output


def test_format_coverage_report_verbose_output() -> None:
    """
    Test verbose formatting with detailed missing test list.
    """
    # Arrange
    missing1 = MissingTest("src/a.py", "tests/test_a.py", "src")
    missing2 = MissingTest("src/b.py", "tests/test_b.py", "src")
    report = CoverageReport(
        total_source_files=10,
        files_with_tests=8,
        missing_tests=[missing1, missing2],
        coverage_percentage=80.0,
    )

    # Act
    output = format_coverage_report(report, verbose=True)

    # Assert
    assert "Missing Tests by Module:" in output
    assert "src: 2 missing" in output
    assert "src/a.py" in output
    assert "src/b.py" in output
    assert "tests/test_a.py" in output


def test_format_coverage_report_show_limit() -> None:
    """
    Test show_limit parameter limits output.
    """
    # Arrange
    missing_tests = [
        MissingTest(f"src/file{i}.py", f"tests/test_file{i}.py", "src")
        for i in range(30)
    ]
    report = CoverageReport(
        total_source_files=30,
        files_with_tests=0,
        missing_tests=missing_tests,
        coverage_percentage=0.0,
    )

    # Act
    output = format_coverage_report(report, verbose=True, show_limit=5)

    # Assert
    assert "... and 25 more" in output
    assert "file0.py" in output
    assert "file4.py" in output
    assert "file10.py" not in output  # Should be truncated


def test_format_coverage_report_invalid_report_type_raises_error() -> None:
    """
    Test TypeError for invalid report parameter.
    """
    # Arrange
    invalid_report = "not_a_report"
    expected_message = "report must be CoverageReport, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_coverage_report(invalid_report)


def test_format_coverage_report_invalid_verbose_type_raises_error() -> None:
    """
    Test TypeError for invalid verbose parameter.
    """
    # Arrange
    report = CoverageReport(
        total_source_files=0,
        files_with_tests=0,
        missing_tests=[],
        coverage_percentage=0.0,
    )
    expected_message = "verbose must be bool, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_coverage_report(report, verbose="yes")


def test_format_coverage_report_invalid_show_limit_type_raises_error() -> None:
    """
    Test TypeError for invalid show_limit parameter.
    """
    # Arrange
    report = CoverageReport(
        total_source_files=0,
        files_with_tests=0,
        missing_tests=[],
        coverage_percentage=0.0,
    )
    expected_message = "show_limit must be int, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_coverage_report(report, show_limit="10")


def test_format_coverage_report_empty_missing_tests() -> None:
    """
    Test formatting when there are no missing tests.
    """
    # Arrange
    report = CoverageReport(
        total_source_files=10,
        files_with_tests=10,
        missing_tests=[],
        coverage_percentage=100.0,
    )

    # Act
    output = format_coverage_report(report)

    # Assert
    assert "Coverage: 100.0%" in output
    assert "Missing Tests: 0" in output
    assert "Missing Tests by Module:" not in output


def test_format_coverage_report_multiple_modules() -> None:
    """
    Test formatting with missing tests from multiple modules.
    """
    # Arrange
    missing_tests = [
        MissingTest("utils/helper.py", "tests/utils/test_helper.py", "utils"),
        MissingTest("core/main.py", "tests/core/test_main.py", "core"),
        MissingTest("core/config.py", "tests/core/test_config.py", "core"),
    ]
    report = CoverageReport(
        total_source_files=10,
        files_with_tests=7,
        missing_tests=missing_tests,
        coverage_percentage=70.0,
    )

    # Act
    output = format_coverage_report(report, verbose=True)

    # Assert
    assert "core: 2 missing" in output
    assert "utils: 1 missing" in output
    assert "core/main.py" in output
    assert "core/config.py" in output
    assert "utils/helper.py" in output
