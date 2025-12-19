"""
Project validation submodule.

This module provides project structure validation functionality.
"""

from .validate_project_structure import (
    validate_project_structure,
    ValidationResult,
    ValidationIssue,
)

__all__ = ["validate_project_structure", "ValidationResult", "ValidationIssue"]
