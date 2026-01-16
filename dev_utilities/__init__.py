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
from .code_analysis.count_code_lines import (
    CodeLineCount,
    count_code_lines,
    count_code_lines_directory,
)
from .code_analysis.generate_dependency_graph import generate_dependency_graph
from .code_analysis.get_code_statistics import (
    CodeStatistics,
    format_statistics,
    get_code_statistics,
)
from .license_templates.generate_license import (
    LicenseType,
    generate_license,
    save_license_file,
)
from .project_validation.find_missing_tests import (
    CoverageReport,
    MissingTest,
    find_missing_tests,
    format_coverage_report,
)
from .project_validation.validate_project_structure import (
    ValidationIssue,
    ValidationResult,
    format_validation_result,
    validate_project_structure,
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
    "CoverageReport",
    "LicenseType",
]
