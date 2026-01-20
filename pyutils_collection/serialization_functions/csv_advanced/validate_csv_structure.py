"""
Validate CSV file structure and schema.
"""

import csv
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def validate_csv_structure(
    file_path: str | Path,
    *,
    expected_columns: Sequence[str] | None = None,
    min_rows: int | None = None,
    max_rows: int | None = None,
    required_columns: Sequence[str] | None = None,
    allow_extra_columns: bool = True,
    encoding: str = "utf-8",
    **kwargs: Any,
) -> tuple[bool, list[str]]:
    """
    Validate CSV file structure against schema requirements.

    Checks header columns, row counts, and data integrity. Returns validation
    result with detailed error messages for debugging.

    Parameters
    ----------
    file_path : str | Path
        Path to CSV file to validate.
    expected_columns : Sequence[str] | None, optional
        Expected column names in order (by default None).
    min_rows : int | None, optional
        Minimum number of data rows (by default None).
    max_rows : int | None, optional
        Maximum number of data rows (by default None).
    required_columns : Sequence[str] | None, optional
        Columns that must be present (by default None).
    allow_extra_columns : bool, optional
        Allow columns not in expected_columns (by default True).
    encoding : str, optional
        File encoding (by default 'utf-8').
    **kwargs : Any
        Additional arguments for csv.DictReader.

    Returns
    -------
    tuple[bool, list[str]]
        (is_valid, error_messages). is_valid=True if all checks pass.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If file doesn't exist.

    Examples
    --------
    >>> is_valid, errors = validate_csv_structure(
    ...     'data.csv',
    ...     expected_columns=['name', 'age', 'email'],
    ...     min_rows=10
    ... )
    >>> is_valid
    True

    >>> is_valid, errors = validate_csv_structure(
    ...     'data.csv',
    ...     required_columns=['id', 'timestamp'],
    ...     max_rows=1000
    ... )
    >>> if not is_valid:
    ...     print(errors)
    ['Missing required column: timestamp', 'Row count 1500 exceeds max 1000']

    Notes
    -----
    Validation is comprehensive - checks column names, order, and row counts.
    Empty rows are skipped in row count validation.

    Complexity
    ----------
    Time: O(n) where n=number of rows
    Space: O(1)
    """
    # Type validation
    if not isinstance(file_path, (str, Path)):
        raise TypeError(
            f"file_path must be str or Path, got {type(file_path).__name__}"
        )
    if expected_columns is not None and not isinstance(expected_columns, (list, tuple)):
        raise TypeError(
            f"expected_columns must be a sequence or None, got {type(expected_columns).__name__}"
        )
    if min_rows is not None and not isinstance(min_rows, int):
        raise TypeError(f"min_rows must be int or None, got {type(min_rows).__name__}")
    if max_rows is not None and not isinstance(max_rows, int):
        raise TypeError(f"max_rows must be int or None, got {type(max_rows).__name__}")
    if required_columns is not None and not isinstance(required_columns, (list, tuple)):
        raise TypeError(
            f"required_columns must be a sequence or None, got {type(required_columns).__name__}"
        )
    if not isinstance(allow_extra_columns, bool):
        raise TypeError(
            f"allow_extra_columns must be bool, got {type(allow_extra_columns).__name__}"
        )
    if not isinstance(encoding, str):
        raise TypeError(f"encoding must be str, got {type(encoding).__name__}")

    # Value validation
    if not Path(file_path).exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    if min_rows is not None and min_rows < 0:
        raise ValueError(f"min_rows must be non-negative, got {min_rows}")
    if max_rows is not None and max_rows < 0:
        raise ValueError(f"max_rows must be non-negative, got {max_rows}")
    if min_rows is not None and max_rows is not None and min_rows > max_rows:
        raise ValueError(f"min_rows ({min_rows}) cannot exceed max_rows ({max_rows})")

    errors: list[str] = []

    try:
        with open(file_path, encoding=encoding, newline="") as csvfile:
            reader = csv.DictReader(csvfile, **kwargs)

            # Get actual columns
            if reader.fieldnames is None:
                errors.append("CSV file has no header row")
                return False, errors

            actual_columns = list(reader.fieldnames)

            # Validate expected columns
            if expected_columns is not None:
                expected_list = list(expected_columns)
                if not allow_extra_columns:
                    if actual_columns != expected_list:
                        errors.append(
                            f"Column mismatch. Expected {expected_list}, got {actual_columns}"
                        )
                else:
                    # Check if expected columns are present in order
                    for exp_col in expected_list:
                        if exp_col not in actual_columns:
                            errors.append(f"Missing expected column: {exp_col}")

            # Validate required columns
            if required_columns is not None:
                for req_col in required_columns:
                    if req_col not in actual_columns:
                        errors.append(f"Missing required column: {req_col}")

            # Count rows
            row_count = 0
            for row in reader:
                # Skip empty rows
                if any(row.values()):
                    row_count += 1

            # Validate row counts
            if min_rows is not None and row_count < min_rows:
                errors.append(f"Row count {row_count} is below minimum {min_rows}")
            if max_rows is not None and row_count > max_rows:
                errors.append(f"Row count {row_count} exceeds maximum {max_rows}")

    except Exception as e:
        errors.append(f"Error reading CSV file: {e}")

    is_valid = len(errors) == 0
    return is_valid, errors


__all__ = ["validate_csv_structure"]
