"""
Project validation submodule.

This module provides project structure validation functionality.
"""

from .find_missing_tests import (
    CoverageReport,
    MissingTest,
    find_missing_tests,
    format_coverage_report,
)
from .validate_project_structure import (
    ValidationIssue,
    ValidationResult,
    validate_project_structure,
)

__all__ = [
    "validate_project_structure",
    "ValidationResult",
    "ValidationIssue",
    "find_missing_tests",
    "format_coverage_report",
    "MissingTest",
    "CoverageReport",
]
