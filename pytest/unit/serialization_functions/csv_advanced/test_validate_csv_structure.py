"""
Unit tests for validate_csv_structure function.
"""

import csv
import tempfile
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.serialization]
from serialization_functions.csv_advanced.validate_csv_structure import (
    validate_csv_structure,
)


def test_validate_csv_structure_valid_structure() -> None:
    """
    Test valid CSV structure passes validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age", "email"])
            for i in range(15):
                writer.writerow([f"Person{i}", str(20 + i), f"person{i}@example.com"])

        is_valid, errors = validate_csv_structure(
            file_path,
            expected_columns=["name", "age", "email"],
            min_rows=10,
            max_rows=20,
        )

        assert is_valid is True
        assert len(errors) == 0


def test_validate_csv_structure_required_columns_present() -> None:
    """
    Test validation with required columns present.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age", "email"])
            writer.writerow(["1", "Alice", "30", "alice@example.com"])

        is_valid, errors = validate_csv_structure(
            file_path, required_columns=["id", "name"]
        )

        assert is_valid is True
        assert len(errors) == 0


def test_validate_csv_structure_extra_columns_allowed() -> None:
    """
    Test validation allows extra columns when configured.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age", "extra"])
            writer.writerow(["1", "Alice", "30", "data"])

        is_valid, errors = validate_csv_structure(
            file_path, expected_columns=["id", "name"], allow_extra_columns=True
        )

        assert is_valid is True


def test_validate_csv_structure_row_count_within_limits() -> None:
    """
    Test validation passes when row count is within limits.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "value"])
            for i in range(25):
                writer.writerow([str(i), f"value{i}"])

        is_valid, errors = validate_csv_structure(file_path, min_rows=20, max_rows=30)

        assert is_valid is True


def test_validate_csv_structure_missing_column() -> None:
    """
    Test missing required column fails validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age"])
            writer.writerow(["Alice", "30"])

        is_valid, errors = validate_csv_structure(
            file_path, required_columns=["name", "age", "email"]
        )

        assert is_valid is False
        assert any("Missing required column: email" in err for err in errors)


def test_validate_csv_structure_too_few_rows() -> None:
    """
    Test too few rows fails validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "value"])
            writer.writerow(["1", "A"])
            writer.writerow(["2", "B"])

        is_valid, errors = validate_csv_structure(file_path, min_rows=10)

        assert is_valid is False
        assert any("below minimum" in err for err in errors)


def test_validate_csv_structure_too_many_rows() -> None:
    """
    Test too many rows fails validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id"])
            for i in range(100):
                writer.writerow([str(i)])

        is_valid, errors = validate_csv_structure(file_path, max_rows=50)

        assert is_valid is False
        assert any("exceeds maximum" in err for err in errors)


def test_validate_csv_structure_column_mismatch_strict() -> None:
    """
    Test column mismatch with strict validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "extra"])
            writer.writerow(["1", "Alice", "data"])

        is_valid, errors = validate_csv_structure(
            file_path, expected_columns=["id", "name"], allow_extra_columns=False
        )

        assert is_valid is False
        assert any("Column mismatch" in err for err in errors)


def test_validate_csv_structure_invalid_type_file_path() -> None:
    """
    Test TypeError for invalid file_path type.
    """
    with pytest.raises(TypeError, match="file_path must be str or Path"):
        validate_csv_structure(123)  # type: ignore


def test_validate_csv_structure_invalid_type_min_rows() -> None:
    """
    Test TypeError for invalid min_rows type.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "data.csv"
        file_path.touch()

        with pytest.raises(TypeError, match="min_rows must be int or None"):
            validate_csv_structure(file_path, min_rows="10")  # type: ignore


def test_validate_csv_structure_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        validate_csv_structure("/nonexistent/file.csv")
