"""
Project validation submodule.

This module provides project structure validation functionality.
"""

from .validate_project_structure import (
    validate_project_structure,
    ValidationResult,
    ValidationIssue,
)
from .find_missing_tests import (
    find_missing_tests,
    format_coverage_report,
    MissingTest,
    CoverageReport,
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
