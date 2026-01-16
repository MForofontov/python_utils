"""Tests for filter_parquet module."""

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

import pytest
from serialization_functions.parquet_operations.filter_parquet import filter_parquet


def test_filter_parquet_equal_operator(tmp_path: Path) -> None:
    """
    Test case 1: Test filtering with equal operator.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice", "Bob"], "age": [30, 25]})
    pq.write_table(table, file_path)

    filters = [("name", "=", "Alice")]

    # Act
    result = filter_parquet(str(file_path), filters)

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_filter_parquet_greater_than_operator(tmp_path: Path) -> None:
    """
    Test case 2: Test filtering with greater than operator.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"age": [20, 30, 40]})
    pq.write_table(table, file_path)

    filters = [("age", ">", 25)]

    # Act
    result = filter_parquet(str(file_path), filters)

    # Assert
    assert len(result) == 2
    assert all(r["age"] > 25 for r in result)


def test_filter_parquet_in_operator(tmp_path: Path) -> None:
    """
    Test case 3: Test filtering with 'in' operator.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"city": ["NYC", "LA", "Chicago"]})
    pq.write_table(table, file_path)

    filters = [("city", "in", ["NYC", "LA"])]

    # Act
    result = filter_parquet(str(file_path), filters)

    # Assert
    assert len(result) == 2
    assert all(r["city"] in ["NYC", "LA"] for r in result)


def test_filter_parquet_multiple_conditions(tmp_path: Path) -> None:
    """
    Test case 4: Test filtering with multiple conditions.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35]})
    pq.write_table(table, file_path)

    filters = [("age", ">=", 30), ("name", "!=", "Charlie")]

    # Act
    result = filter_parquet(str(file_path), filters)

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_filter_parquet_with_column_selection(tmp_path: Path) -> None:
    """
    Test case 5: Test filtering with specific columns.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice"], "age": [30], "city": ["NYC"]})
    pq.write_table(table, file_path)

    filters = [("age", "=", 30)]

    # Act
    result = filter_parquet(str(file_path), filters, columns=["name", "city"])

    # Assert
    assert len(result) == 1
    assert "name" in result[0]
    assert "city" in result[0]
    assert "age" not in result[0]


def test_filter_parquet_invalid_file_path_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid file_path type.
    """
    # Arrange
    filters = [("col", "=", "val")]

    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        filter_parquet(123, filters)


def test_filter_parquet_invalid_columns_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test TypeError for invalid columns type.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act & Assert
    with pytest.raises(TypeError, match="filters must be a list"):
        filter_parquet(str(file_path), "invalid")


def test_filter_parquet_invalid_filter_format_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test ValueError for invalid filter format.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act & Assert
    with pytest.raises(ValueError, match="Each filter must be a tuple"):
        filter_parquet(str(file_path), [("col", "=")])  # Missing value


def test_filter_parquet_unsupported_operator_raises_error(tmp_path: Path) -> None:
    """
    Test case 9: Test ValueError for unsupported operator.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act & Assert
    with pytest.raises(ValueError, match="Unsupported operator"):
        filter_parquet(str(file_path), [("col", "INVALID", 1)])
