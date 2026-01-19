"""Tests for read_parquet module."""

from pathlib import Path

try:
    import pyarrow as pa
    import pyarrow.parquet as pq

    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    pa = None  # type: ignore
    pq = None  # type: ignore

import pytest
from serialization_functions.parquet_operations.read_parquet import read_parquet

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")


def test_read_parquet_basic(tmp_path: Path) -> None:
    """
    Test case 1: Test basic reading of Parquet file.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice", "Bob"], "age": [30, 25]})
    pq.write_table(table, file_path)

    # Act
    data = read_parquet(str(file_path))

    # Assert
    assert len(data) == 2
    assert data[0] == {"name": "Alice", "age": 30}
    assert data[1] == {"name": "Bob", "age": 25}


def test_read_parquet_specific_columns(tmp_path: Path) -> None:
    """
    Test case 2: Test reading specific columns only.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice"], "age": [30], "city": ["NYC"]})
    pq.write_table(table, file_path)

    # Act
    data = read_parquet(str(file_path), columns=["name", "city"])

    # Assert
    assert len(data) == 1
    assert set(data[0].keys()) == {"name", "city"}
    assert "age" not in data[0]


def test_read_parquet_single_column(tmp_path: Path) -> None:
    """
    Test case 3: Test reading single column.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"value": [1, 2, 3]})
    pq.write_table(table, file_path)

    # Act
    data = read_parquet(str(file_path), columns=["value"])

    # Assert
    assert all(isinstance(row, dict) for row in data)
    assert all("value" in row for row in data)


def test_read_parquet_empty_table(tmp_path: Path) -> None:
    """
    Test case 4: Test reading empty Parquet file.
    """
    # Arrange

    file_path = tmp_path / "empty.parquet"
    table = pa.table({"col": pa.array([], type=pa.int64())})
    pq.write_table(table, file_path)

    # Act
    data = read_parquet(str(file_path))

    # Assert
    assert isinstance(data, list)
    assert len(data) == 0


def test_read_parquet_various_types(tmp_path: Path) -> None:
    """
    Test case 5: Test reading Parquet with various data types.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table(
        {
            "int_col": [1, 2],
            "float_col": [1.1, 2.2],
            "str_col": ["a", "b"],
            "bool_col": [True, False],
        }
    )
    pq.write_table(table, file_path)

    # Act
    data = read_parquet(str(file_path))

    # Assert
    assert len(data) == 2
    assert isinstance(data[0]["int_col"], int)
    assert isinstance(data[0]["float_col"], float)
    assert isinstance(data[0]["str_col"], str)
    assert isinstance(data[0]["bool_col"], bool)


def test_read_parquet_invalid_file_path_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid file_path type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        read_parquet(123)


def test_read_parquet_invalid_columns_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test TypeError for invalid columns type.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act & Assert
    with pytest.raises(TypeError, match="columns must be a list or None"):
        read_parquet(str(file_path), columns="invalid")


def test_read_parquet_invalid_column_element_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test TypeError for invalid column element type.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act & Assert
    with pytest.raises(TypeError, match="all elements in columns must be strings"):
        read_parquet(str(file_path), columns=[123])


def test_read_parquet_nonexistent_file_raises_error(tmp_path: Path) -> None:
    """
    Test case 9: Test error for non-existent file.
    """
    # Arrange
    nonexistent = tmp_path / "does_not_exist.parquet"

    # Act & Assert
    with pytest.raises(Exception):  # noqa: B017 - pyarrow raises FileNotFoundError
        read_parquet(str(nonexistent))
