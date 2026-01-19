"""Validate Python project structure and conventions."""

from pathlib import Path
from typing import NamedTuple


class ValidationIssue(NamedTuple):
    """
    Represents a validation issue found in the project.

    Attributes
    ----------
    severity : str
        Severity level ('error', 'warning', 'info').
    category : str
        Issue category ('structure', 'naming', 'documentation', 'testing').
    message : str
        Description of the issue.
    path : str | None
        File or directory path related to the issue.
    """

    severity: str
    category: str
    message: str
    path: str | None = None


class ValidationResult(NamedTuple):
    """
    Contains the results of project validation.

    Attributes
    ----------
    is_valid : bool
        Whether the project passes all validations.
    issues : list[ValidationIssue]
        List of validation issues found.
    score : float
        Validation score (0-100).
    """

    is_valid: bool
    issues: list[ValidationIssue]
    score: float


def validate_project_structure(
    project_path: str | Path,
    strict: bool = False,
    check_tests: bool = True,
) -> ValidationResult:
    """
    Validate Python project structure against best practices.

    Checks for presence of required files (README, LICENSE, __init__.py),
    proper naming conventions, documentation, and test structure.

    Parameters
    ----------
    project_path : str | Path
        Path to the project directory to validate.
    strict : bool, optional
        Whether to enforce strict validation rules (by default False).
    check_tests : bool, optional
        Whether to check for test files (by default True).

    Returns
    -------
    ValidationResult
        Named tuple containing validation results and issues.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If project_path doesn't exist.
    ValueError
        If project_path is not a directory.

    Examples
    --------
    >>> result = validate_project_structure('my_project')  # doctest: +SKIP
    >>> if result.is_valid:  # doctest: +SKIP
    ...     print("Project structure is valid!")
    >>> else:  # doctest: +SKIP
    ...     for issue in result.issues:
    ...         print(f"{issue.severity}: {issue.message}")

    Notes
    -----
    - Checks for README, LICENSE, setup.py/pyproject.toml
    - Validates naming conventions (snake_case for modules)
    - Verifies __init__.py files in packages
    - Optionally checks for test directory structure
    - Strict mode enforces additional best practices

    Complexity
    ----------
    Time: O(n), Space: O(n)
    where n is the number of files in the project
    """
    # Input validation
    if not isinstance(project_path, (str, Path)):
        raise TypeError(
            f"project_path must be str or Path, got {type(project_path).__name__}"
        )
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be bool, got {type(strict).__name__}")
    if not isinstance(check_tests, bool):
        raise TypeError(f"check_tests must be bool, got {type(check_tests).__name__}")

    project_path = Path(project_path)

    if not project_path.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")

    if not project_path.is_dir():
        raise ValueError(f"Project path must be a directory: {project_path}")

    issues: list[ValidationIssue] = []

    # Check for required files
    _check_required_files(project_path, issues, strict)

    # Check naming conventions
    _check_naming_conventions(project_path, issues)

    # Check for __init__.py in packages
    _check_init_files(project_path, issues)

    # Check documentation
    _check_documentation(project_path, issues, strict)

    # Check test structure
    if check_tests:
        _check_test_structure(project_path, issues)

    # Calculate score
    error_count = sum(1 for issue in issues if issue.severity == "error")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")
    info_count = sum(1 for issue in issues if issue.severity == "info")

    # Score calculation: errors -20, warnings -10, info -5
    max_deductions = error_count * 20 + warning_count * 10 + info_count * 5
    score = max(0.0, 100.0 - max_deductions)

    is_valid = error_count == 0 and (not strict or warning_count == 0)

    return ValidationResult(is_valid=is_valid, issues=issues, score=score)


def _check_required_files(
    project_path: Path, issues: list[ValidationIssue], strict: bool
) -> None:
    """Check for required project files."""
    # README file
    readme_files = list(project_path.glob("README.*"))
    if not readme_files:
        issues.append(
            ValidationIssue(
                severity="error",
                category="documentation",
                message="Missing README file (README.md, README.rst, or README.txt)",
                path=str(project_path),
            )
        )

    # LICENSE file
    license_file = project_path / "LICENSE"
    if not license_file.exists():
        severity = "error" if strict else "warning"
        issues.append(
            ValidationIssue(
                severity=severity,
                category="documentation",
                message="Missing LICENSE file",
                path=str(project_path),
            )
        )

    # Setup configuration
    has_setup_py = (project_path / "setup.py").exists()
    has_pyproject = (project_path / "pyproject.toml").exists()
    if not has_setup_py and not has_pyproject:
        severity = "warning" if not strict else "error"
        issues.append(
            ValidationIssue(
                severity=severity,
                category="structure",
                message="Missing setup.py or pyproject.toml",
                path=str(project_path),
            )
        )

    # .gitignore
    if not (project_path / ".gitignore").exists():
        issues.append(
            ValidationIssue(
                severity="info",
                category="structure",
                message="Missing .gitignore file",
                path=str(project_path),
            )
        )


def _check_naming_conventions(
    project_path: Path, issues: list[ValidationIssue]
) -> None:
    """Check Python module naming conventions."""
    for py_file in project_path.rglob("*.py"):
        # Skip __pycache__ and hidden directories
        if "__pycache__" in py_file.parts or any(
            part.startswith(".") for part in py_file.parts[len(project_path.parts) :]
        ):
            continue

        file_name = py_file.stem
        # Allow __init__, __main__, etc.
        if file_name.startswith("__") and file_name.endswith("__"):
            continue

        # Check for snake_case
        if not file_name.islower() or "-" in file_name:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    category="naming",
                    message=f"Module name should be lowercase snake_case: {file_name}",
                    path=str(py_file),
                )
            )


def _check_init_files(project_path: Path, issues: list[ValidationIssue]) -> None:
    """Check for __init__.py files in package directories."""
    # Find directories that contain Python files
    python_dirs: set[Path] = set()
    for py_file in project_path.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue
        parent = py_file.parent
        if parent != project_path:
            python_dirs.add(parent)

    # Check each directory has __init__.py
    for py_dir in python_dirs:
        # Skip hidden directories and __pycache__
        if any(
            part.startswith(".") or part == "__pycache__"
            for part in py_dir.parts[len(project_path.parts) :]
        ):
            continue

        init_file = py_dir / "__init__.py"
        if not init_file.exists():
            issues.append(
                ValidationIssue(
                    severity="warning",
                    category="structure",
                    message="Package directory missing __init__.py",
                    path=str(py_dir),
                )
            )


def _check_documentation(
    project_path: Path, issues: list[ValidationIssue], strict: bool
) -> None:
    """Check for documentation files."""
    docs_dir = project_path / "docs"
    if not docs_dir.exists() and strict:
        issues.append(
            ValidationIssue(
                severity="info",
                category="documentation",
                message="No docs directory found",
                path=str(project_path),
            )
        )

    # Check for CHANGELOG
    changelog_files = list(project_path.glob("CHANGELOG.*")) + list(
        project_path.glob("HISTORY.*")
    )
    if not changelog_files and strict:
        issues.append(
            ValidationIssue(
                severity="info",
                category="documentation",
                message="No CHANGELOG file found",
                path=str(project_path),
            )
        )


def _check_test_structure(project_path: Path, issues: list[ValidationIssue]) -> None:
    """Check test directory structure."""
    # Look for test directories
    test_dirs = [
        project_path / "tests",
        project_path / "test",
        project_path / "pytest",
    ]

    has_test_dir = any(d.exists() and d.is_dir() for d in test_dirs)

    # Look for test files anywhere
    test_files = list(project_path.rglob("test_*.py")) + list(
        project_path.rglob("*_test.py")
    )

    if not has_test_dir and not test_files:
        issues.append(
            ValidationIssue(
                severity="warning",
                category="testing",
                message="No test directory or test files found",
                path=str(project_path),
            )
        )
    elif not has_test_dir:
        issues.append(
            ValidationIssue(
                severity="info",
                category="testing",
                message="Test files found but no dedicated test directory",
                path=str(project_path),
            )
        )


def format_validation_result(result: ValidationResult, verbose: bool = True) -> str:
    """
    Format validation result as a readable report.

    Parameters
    ----------
    result : ValidationResult
        Validation result to format.
    verbose : bool, optional
        Include detailed issue information (by default True).

    Returns
    -------
    str
        Formatted validation report.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> result = validate_project_structure('my_project')  # doctest: +SKIP
    >>> report = format_validation_result(result)  # doctest: +SKIP
    >>> print(report)  # doctest: +SKIP

    Complexity
    ----------
    Time: O(n), Space: O(n)
    where n is the number of validation issues
    """
    if not isinstance(result, ValidationResult):
        raise TypeError(f"result must be ValidationResult, got {type(result).__name__}")
    if not isinstance(verbose, bool):
        raise TypeError(f"verbose must be bool, got {type(verbose).__name__}")

    lines = [
        "Project Validation Report",
        "=" * 50,
        "",
        f"Status: {'✓ PASS' if result.is_valid else '✗ FAIL'}",
        f"Score: {result.score:.1f}/100",
        "",
    ]

    if result.issues:
        # Group issues by severity
        errors = [i for i in result.issues if i.severity == "error"]
        warnings = [i for i in result.issues if i.severity == "warning"]
        infos = [i for i in result.issues if i.severity == "info"]

        lines.append(f"Issues Found: {len(result.issues)}")
        lines.append(f"  Errors: {len(errors)}")
        lines.append(f"  Warnings: {len(warnings)}")
        lines.append(f"  Info: {len(infos)}")
        lines.append("")

        if verbose:
            if errors:
                lines.append("ERRORS:")
                for issue in errors:
                    lines.append(f"  ✗ [{issue.category}] {issue.message}")
                    if issue.path:
                        lines.append(f"    Path: {issue.path}")
                lines.append("")

            if warnings:
                lines.append("WARNINGS:")
                for issue in warnings:
                    lines.append(f"  ⚠ [{issue.category}] {issue.message}")
                    if issue.path:
                        lines.append(f"    Path: {issue.path}")
                lines.append("")

            if infos:
                lines.append("INFO:")
                for issue in infos:
                    lines.append(f"  ℹ [{issue.category}] {issue.message}")
                    if issue.path:
                        lines.append(f"    Path: {issue.path}")
                lines.append("")
    else:
        lines.append("No issues found! ✓")
        lines.append("")

    return "\n".join(lines)


__all__ = [
    "validate_project_structure",
    "format_validation_result",
    "ValidationResult",
    "ValidationIssue",
]
