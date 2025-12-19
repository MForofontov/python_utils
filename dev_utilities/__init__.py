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
from .code_analysis.count_code_lines import count_code_lines
from .code_analysis.generate_dependency_graph import generate_dependency_graph
from .code_analysis.get_code_statistics import get_code_statistics
from .license_templates.generate_license import generate_license
from .project_validation.validate_project_structure import (
    validate_project_structure,
)

__all__ = [
    # Submodules
    "code_analysis",
    "license_templates",
    "project_validation",
    # Code analysis functions
    "count_code_lines",
    "generate_dependency_graph",
    "get_code_statistics",
    # License functions
    "generate_license",
    # Project validation functions
    "validate_project_structure",
]

__version__ = "1.0.0"
