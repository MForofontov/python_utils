"""Tests for append_parquet module."""

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

import pytest
from serialization_functions.parquet_operations.append_parquet import append_parquet


def test_append_parquet_to_new_file(tmp_path: Path) -> None:
    """
    Test case 1: Test appending to non-existent file creates new file.
    """
    # Arrange

    file_path = tmp_path / "new.parquet"
    data = [{"name": "Alice", "age": 30}]

    # Act
    append_parquet(data, str(file_path))

    # Assert
    assert file_path.exists()
    table = pq.read_table(file_path)
    assert table.num_rows == 1


def test_append_parquet_to_existing_file(tmp_path: Path) -> None:
    """
    Test case 2: Test appending to existing Parquet file.
    """
    # Arrange

    file_path = tmp_path / "existing.parquet"
    table = pa.table({"name": ["Alice"], "age": [30]})
    pq.write_table(table, file_path)

    new_data = [{"name": "Bob", "age": 25}]

    # Act
    append_parquet(new_data, str(file_path))

    # Assert
    table = pq.read_table(file_path)
    assert table.num_rows == 2
    data = table.to_pylist()
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"


def test_append_parquet_multiple_rows(tmp_path: Path) -> None:
    """
    Test case 3: Test appending multiple rows at once.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"value": [1]})
    pq.write_table(table, file_path)

    new_data = [{"value": 2}, {"value": 3}, {"value": 4}]

    # Act
    append_parquet(new_data, str(file_path))

    # Assert
    table = pq.read_table(file_path)
    assert table.num_rows == 4


def test_append_parquet_with_compression(tmp_path: Path) -> None:
    """
    Test case 4: Test appending with custom compression.
    """
    # Arrange
    file_path = tmp_path / "compressed.parquet"
    data = [{"value": 1}]

    # Act
    append_parquet(data, str(file_path), compression="gzip")

    # Assert
    assert file_path.exists()


def test_append_parquet_creates_parent_directories(tmp_path: Path) -> None:
    """
    Test case 5: Test that parent directories are created.
    """
    # Arrange
    file_path = tmp_path / "nested" / "output.parquet"
    data = [{"value": 1}]

    # Act
    append_parquet(data, str(file_path))

    # Assert
    assert file_path.exists()


def test_append_parquet_invalid_data_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 6: Test TypeError for invalid data type.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(TypeError, match="data must be a list"):
        append_parquet("invalid", str(file_path))


def test_append_parquet_empty_data_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test ValueError for empty data.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(ValueError, match="data cannot be empty"):
        append_parquet([], str(file_path))


def test_append_parquet_schema_mismatch_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test ValueError for schema mismatch.
    """
    # Arrange

    file_path = tmp_path / "existing.parquet"
    table = pa.table({"name": ["Alice"]})
    pq.write_table(table, file_path)

    new_data = [{"age": 30}]  # Different schema

    # Act & Assert
    with pytest.raises(ValueError, match="Schema mismatch"):
        append_parquet(new_data, str(file_path))


def test_append_parquet_invalid_file_path_type_raises_error() -> None:
    """
    Test case 9: Test TypeError for invalid file_path type.
    """
    # Arrange
    data = [{"value": 1}]

    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        append_parquet(data, 123)


def test_append_parquet_invalid_data_element_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 10: Test TypeError for invalid data element type.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(TypeError, match="all elements in data must be dictionaries"):
        append_parquet(["invalid"], str(file_path))
