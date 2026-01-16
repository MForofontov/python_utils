"""Tests for write_parquet module."""

from pathlib import Path

import pyarrow.parquet as pq

import pytest
from serialization_functions.parquet_operations.write_parquet import write_parquet


def test_write_parquet_basic(tmp_path: Path) -> None:
    """
    Test case 1: Test basic writing to Parquet file.
    """
    # Arrange

    file_path = tmp_path / "output.parquet"
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

    # Act
    write_parquet(data, str(file_path))

    # Assert
    assert file_path.exists()
    table = pq.read_table(file_path)
    assert table.num_rows == 2
    assert table.num_columns == 2


def test_write_parquet_with_compression(tmp_path: Path) -> None:
    """
    Test case 2: Test writing with different compression codecs.
    """
    # Arrange
    file_path = tmp_path / "compressed.parquet"
    data = [{"value": i} for i in range(100)]

    # Act
    write_parquet(data, str(file_path), compression="gzip")

    # Assert
    assert file_path.exists()


def test_write_parquet_no_compression(tmp_path: Path) -> None:
    """
    Test case 3: Test writing without compression.
    """
    # Arrange
    file_path = tmp_path / "uncompressed.parquet"
    data = [{"value": 1}]

    # Act
    write_parquet(data, str(file_path), compression="none")

    # Assert
    assert file_path.exists()


def test_write_parquet_creates_parent_directories(tmp_path: Path) -> None:
    """
    Test case 4: Test that parent directories are created.
    """
    # Arrange
    file_path = tmp_path / "nested" / "folder" / "output.parquet"
    data = [{"value": 1}]

    # Act
    write_parquet(data, str(file_path))

    # Assert
    assert file_path.exists()


def test_write_parquet_various_types(tmp_path: Path) -> None:
    """
    Test case 5: Test writing various data types.
    """
    # Arrange

    file_path = tmp_path / "types.parquet"
    data = [{"int_val": 1, "float_val": 1.5, "str_val": "text", "bool_val": True}]

    # Act
    write_parquet(data, str(file_path))

    # Assert
    table = pq.read_table(file_path)
    assert table.num_columns == 4


def test_write_parquet_invalid_data_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 6: Test TypeError for invalid data type.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(TypeError, match="data must be a list"):
        write_parquet("invalid", str(file_path))


def test_write_parquet_empty_data_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test ValueError for empty data.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(ValueError, match="data cannot be empty"):
        write_parquet([], str(file_path))


def test_write_parquet_invalid_data_element_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test TypeError for invalid data element type.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"

    # Act & Assert
    with pytest.raises(TypeError, match="all elements in data must be dictionaries"):
        write_parquet(["invalid"], str(file_path))


def test_write_parquet_invalid_file_path_type_raises_error() -> None:
    """
    Test case 9: Test TypeError for invalid file_path type.
    """
    # Arrange
    data = [{"value": 1}]

    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        write_parquet(data, 123)


def test_write_parquet_invalid_compression_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 10: Test TypeError for invalid compression type.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"
    data = [{"value": 1}]

    # Act & Assert
    with pytest.raises(TypeError, match="compression must be a string"):
        write_parquet(data, str(file_path), compression=123)


def test_write_parquet_invalid_compression_value_raises_error(tmp_path: Path) -> None:
    """
    Test case 11: Test ValueError for invalid compression value.
    """
    # Arrange
    file_path = tmp_path / "test.parquet"
    data = [{"value": 1}]

    # Act & Assert
    with pytest.raises(ValueError, match="compression must be one of"):
        write_parquet(data, str(file_path), compression="invalid")
