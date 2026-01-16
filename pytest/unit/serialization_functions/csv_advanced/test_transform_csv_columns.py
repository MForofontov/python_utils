"""
Unit tests for transform_csv_columns function.
"""

import csv
import tempfile
from pathlib import Path

import pytest
from serialization_functions.csv_advanced.transform_csv_columns import (
    transform_csv_columns,
)


def test_transform_csv_columns_column_mapping() -> None:
    """
    Test renaming columns with mapping.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["first_name", "user_age"])
            writer.writerow(["Alice", "30"])
            writer.writerow(["Bob", "25"])

        mapping = {"first_name": "name", "user_age": "age"}
        rows = transform_csv_columns(input_file, output_file, column_mapping=mapping)

        assert rows == 2
        with open(output_file, newline="") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            assert data[0]["name"] == "Alice"
            assert data[0]["age"] == "30"


def test_transform_csv_columns_select_columns() -> None:
    """
    Test selecting specific columns.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age", "email"])
            writer.writerow(["1", "Alice", "30", "alice@example.com"])

        rows = transform_csv_columns(
            input_file, output_file, select_columns=["id", "name"]
        )

        assert rows == 1
        with open(output_file, newline="") as f:
            reader = csv.DictReader(f)
            row = next(reader)
            assert list(row.keys()) == ["id", "name"]
            assert "age" not in row
            assert "email" not in row


def test_transform_csv_columns_transformers() -> None:
    """
    Test applying value transformers.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age", "email"])
            writer.writerow(["Alice", "30", "ALICE@EXAMPLE.COM"])

        transformers = {"age": int, "email": str.lower}
        rows = transform_csv_columns(input_file, output_file, transformers=transformers)

        assert rows == 1
        with open(output_file, newline="") as f:
            reader = csv.DictReader(f)
            row = next(reader)
            assert row["email"] == "alice@example.com"


def test_transform_csv_columns_filter_rows() -> None:
    """
    Test filtering rows with function.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age"])
            writer.writerow(["Alice", "30"])
            writer.writerow(["Bob", "17"])
            writer.writerow(["Charlie", "25"])

        filter_func = lambda row: int(row["age"]) >= 18
        rows = transform_csv_columns(input_file, output_file, filter_func=filter_func)

        assert rows == 2  # Only adults
        with open(output_file, newline="") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            assert len(data) == 2
            assert all(int(row["age"]) >= 18 for row in data)


def test_transform_csv_columns_combined_operations() -> None:
    """
    Test combining mapping, selection, and filtering.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "user_name", "user_age", "status"])
            writer.writerow(["1", "Alice", "30", "active"])
            writer.writerow(["2", "", "25", "active"])
            writer.writerow(["3", "Charlie", "35", "inactive"])

        rows = transform_csv_columns(
            input_file,
            output_file,
            column_mapping={"user_id": "id", "user_name": "name", "user_age": "age"},
            select_columns=["id", "name", "age"],
            transformers={"age": int},
            filter_func=lambda row: row["name"] != "",
        )

        assert rows == 2


def test_transform_csv_columns_no_transformations() -> None:
    """
    Test transformation with no operations applied.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name"])
            writer.writerow(["1", "Alice"])
            writer.writerow(["2", "Bob"])

        rows = transform_csv_columns(input_file, output_file)

        assert rows == 2


def test_transform_csv_columns_invalid_type_input_file() -> None:
    """
    Test TypeError for invalid input_file type.
    """
    with pytest.raises(TypeError, match="input_file must be str or Path"):
        transform_csv_columns(123, "output.csv")  # type: ignore


def test_transform_csv_columns_invalid_type_transformers() -> None:
    """
    Test TypeError for invalid transformers type.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"
        input_file.touch()

        with pytest.raises(TypeError, match="transformers must be dict or None"):
            transform_csv_columns(input_file, output_file, transformers="not_a_dict")  # type: ignore


def test_transform_csv_columns_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "output.csv"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            transform_csv_columns("/nonexistent/file.csv", output_file)


def test_transform_csv_columns_invalid_column_selection() -> None:
    """
    Test ValueError for selecting non-existent column.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.csv"

        with open(input_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name"])
            writer.writerow(["1", "Alice"])

        with pytest.raises(ValueError, match="not found in output columns"):
            transform_csv_columns(
                input_file, output_file, select_columns=["nonexistent"]
            )
