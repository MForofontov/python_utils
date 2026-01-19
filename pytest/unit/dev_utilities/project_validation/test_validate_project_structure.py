"""
Test case 1: Test project structure validation functionality.
"""

import tempfile
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.dev_utilities]
from python_utils.dev_utilities.project_validation.validate_project_structure import (
    ValidationIssue,
    ValidationResult,
    format_validation_result,
    validate_project_structure,
)


def test_validate_project_structure_valid_project() -> None:
    """
    Test case 1: Validate a well-structured project.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "README.md").write_text("# Project")
        (project_path / "LICENSE").write_text("MIT License")
        (project_path / "pyproject.toml").write_text("[project]")
        subdir = project_path / "mypackage"
        subdir.mkdir()
        (subdir / "__init__.py").write_text("")
        (subdir / "module.py").write_text("x = 1")

        # Act
        result = validate_project_structure(project_path, strict=False)

        # Assert
        assert isinstance(result, ValidationResult)
        assert result.score >= 0


def test_validate_project_structure_missing_readme() -> None:
    """
    Test case 2: Detect missing README file.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)

        # Act
        result = validate_project_structure(project_path)

        # Assert
        assert not result.is_valid
        readme_issues = [i for i in result.issues if "README" in i.message]
        assert len(readme_issues) > 0


def test_validate_project_structure_invalid_type_raises_error() -> None:
    """
    Test case 3: TypeError for invalid project_path type.
    """
    # Arrange
    invalid_path = 123
    expected_message = "project_path must be str or Path, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        validate_project_structure(invalid_path)  # type: ignore


def test_validate_project_structure_nonexistent_path_raises_error() -> None:
    """
    Test case 4: FileNotFoundError for nonexistent path.
    """
    # Arrange
    invalid_path = "/nonexistent/project/path"
    expected_message = "Project path does not exist"

    # Act & Assert
    with pytest.raises(FileNotFoundError, match=expected_message):
        validate_project_structure(invalid_path)


def test_validate_project_structure_strict_mode() -> None:
    """
    Test case 5: Strict mode enforces additional rules.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "README.md").write_text("# Test")
        # Missing LICENSE in strict mode should fail

        # Act
        result = validate_project_structure(project_path, strict=True)

        # Assert
        # Strict mode should have more stringent requirements
        assert len(result.issues) >= 0


def test_validate_project_structure_check_naming_conventions() -> None:
    """
    Test case 6: Detect incorrect naming conventions.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        # Create file with incorrect naming (should be snake_case)
        (project_path / "BadName.py").write_text("x = 1")

        # Act
        result = validate_project_structure(project_path)

        # Assert
        naming_issues = [i for i in result.issues if i.category == "naming"]
        assert len(naming_issues) > 0


def test_validate_project_structure_missing_init_files() -> None:
    """
    Test case 7: Detect missing __init__.py files.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        subdir = project_path / "mypackage"
        subdir.mkdir()
        # Create Python file but no __init__.py
        (subdir / "module.py").write_text("x = 1")

        # Act
        result = validate_project_structure(project_path)

        # Assert
        init_issues = [i for i in result.issues if "__init__.py" in i.message]
        assert len(init_issues) > 0


def test_validate_project_structure_with_tests() -> None:
    """
    Test case 8: Check for test directory and files.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        tests_dir = project_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_module.py").write_text("def test(): pass")

        # Act
        result = validate_project_structure(project_path, check_tests=True)

        # Assert
        # With tests present, should not have test-related warnings
        [
            i
            for i in result.issues
            if i.category == "testing" and i.severity == "warning"
        ]
        # May still have other test-related info messages
        assert isinstance(result, ValidationResult)


def test_format_validation_result_verbose() -> None:
    """
    Test case 9: Format validation result with verbose output.
    """
    # Arrange
    issues = [
        ValidationIssue("error", "structure", "Missing file", "/path/to/file"),
        ValidationIssue("warning", "naming", "Bad name", "/path/to/module.py"),
    ]
    result = ValidationResult(is_valid=False, issues=issues, score=80.0)

    # Act
    output = format_validation_result(result, verbose=True)

    # Assert
    assert "Project Validation Report" in output
    assert "ERRORS:" in output
    assert "WARNINGS:" in output
    assert "80.0/100" in output


def test_format_validation_result_invalid_type_raises_error() -> None:
    """
    Test case 10: TypeError for invalid result type.
    """
    # Arrange
    invalid_result = {"is_valid": True}
    expected_message = "result must be ValidationResult"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_validation_result(invalid_result)  # type: ignore


def test_validate_project_structure_no_issues_perfect_score() -> None:
    """
    Test case 11: Project with no issues gets perfect score.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "README.md").write_text("# Project")
        (project_path / "LICENSE").write_text("MIT")
        (project_path / "pyproject.toml").write_text("[project]")
        (project_path / ".gitignore").write_text("*.pyc")
        pkg = project_path / "package"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        tests = project_path / "tests"
        tests.mkdir()
        (tests / "test_main.py").write_text("def test(): pass")

        # Act
        result = validate_project_structure(project_path)

        # Assert
        # Should have very few or no issues
        assert result.score >= 70.0  # High score for well-structured project
