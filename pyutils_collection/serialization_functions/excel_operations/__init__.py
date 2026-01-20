"""
Excel operations module.

Provides utilities for reading, writing, and managing Excel files
using openpyxl. Supports sheet operations, range reading/writing,
and workbook management.
"""

from .auto_format_excel_columns import auto_format_excel_columns
from .create_excel_workbook import create_excel_workbook
from .get_sheet_names import get_sheet_names
from .merge_excel_sheets import merge_excel_sheets
from .read_excel_range import read_excel_range
from .read_excel_sheet import read_excel_sheet
from .transpose_excel_data import transpose_excel_data
from .validate_excel_structure import validate_excel_structure
from .write_excel_range import write_excel_range
from .write_excel_sheet import write_excel_sheet

__all__ = [
    "auto_format_excel_columns",
    "create_excel_workbook",
    "get_sheet_names",
    "merge_excel_sheets",
    "read_excel_range",
    "read_excel_sheet",
    "transpose_excel_data",
    "validate_excel_structure",
    "write_excel_range",
    "write_excel_sheet",
]
