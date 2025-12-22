"""
Development utilities module: Tools for project development and maintenance.

This module provides utilities for analyzing code structure, validating project
conventions, generating licenses, and visualizing dependencies.
"""

# Import from submodules
from . import (
    code_analysis,
    license_templates,
    project_validation,
)

# Import all functions for direct access
from .code_analysis.count_code_lines import count_code_lines, count_code_lines_directory, CodeLineCount
from .code_analysis.generate_dependency_graph import generate_dependency_graph
from .code_analysis.get_code_statistics import get_code_statistics, format_statistics, CodeStatistics
from .license_templates.generate_license import generate_license, save_license_file, LicenseType
from .project_validation.validate_project_structure import (
    validate_project_structure,
    format_validation_result,
    ValidationResult,
    ValidationIssue,
)
from .project_validation.find_missing_tests import (
    find_missing_tests,
    format_coverage_report,
    MissingTest,
    TestCoverageReport,
)

__all__ = [
    # Submodules
    "code_analysis",
    "license_templates",
    "project_validation",
    # Code analysis functions
    "count_code_lines",
    "count_code_lines_directory",
    "generate_dependency_graph",
    "get_code_statistics",
    "format_statistics",
    # License functions
    "generate_license",
    "save_license_file",
    # Project validation functions
    "validate_project_structure",
    "format_validation_result",
    "find_missing_tests",
    "format_coverage_report",
    # Data classes
    "CodeLineCount",
    "CodeStatistics",
    "ValidationResult",
    "ValidationIssue",
    "MissingTest",
    "TestCoverageReport",
    "LicenseType",
]

from .._version import __version__
