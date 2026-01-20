"""Tests for get_parquet_schema module."""

from pathlib import Path

import pytest

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    from pyutils_collection.serialization_functions.parquet_operations.get_parquet_schema import (
        get_parquet_schema,
    )
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    pa = None  # type: ignore
    pq = None  # type: ignore
    get_parquet_schema = None  # type: ignore

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.serialization]


def test_get_parquet_schema_basic(tmp_path: Path) -> None:
    """
    Test case 1: Test getting schema from Parquet file.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice"], "age": [30]})
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    assert isinstance(schema, dict)
    assert "name" in schema
    assert "age" in schema
    assert schema["name"] == "string" or "large_string" in schema["name"]


def test_get_parquet_schema_single_column(tmp_path: Path) -> None:
    """
    Test case 2: Test schema for single column file.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"value": [1, 2, 3]})
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    assert len(schema) == 1
    assert "value" in schema
    assert "int" in schema["value"].lower()


def test_get_parquet_schema_various_types(tmp_path: Path) -> None:
    """
    Test case 3: Test schema with various data types.
    """
    # Arrange

    file_path = tmp_path / "types.parquet"
    table = pa.table(
        {"int_col": [1], "float_col": [1.5], "str_col": ["text"], "bool_col": [True]}
    )
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    assert len(schema) == 4
    assert "int_col" in schema
    assert "float_col" in schema
    assert "str_col" in schema
    assert "bool_col" in schema


def test_get_parquet_schema_many_columns(tmp_path: Path) -> None:
    """
    Test case 4: Test schema for file with many columns.
    """
    # Arrange

    file_path = tmp_path / "wide.parquet"
    data = {f"col{i}": [i] for i in range(20)}
    table = pa.table(data)
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    assert len(schema) == 20
    assert all(f"col{i}" in schema for i in range(20))


def test_get_parquet_schema_preserves_column_order(tmp_path: Path) -> None:
    """
    Test case 5: Test that column order is preserved in schema.
    """
    # Arrange

    file_path = tmp_path / "ordered.parquet"
    table = pa.table({"first": [1], "second": [2], "third": [3]})
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    keys = list(schema.keys())
    assert keys == ["first", "second", "third"]


def test_get_parquet_schema_invalid_file_path_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid file_path type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        get_parquet_schema(123)


def test_get_parquet_schema_nonexistent_file_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test error for non-existent file.
    """
    # Arrange
    nonexistent = tmp_path / "does_not_exist.parquet"

    # Act & Assert
    with pytest.raises(Exception):  # noqa: B017 - pyarrow raises FileNotFoundError
        get_parquet_schema(str(nonexistent))


def test_get_parquet_schema_invalid_file_format_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test error for invalid Parquet file.
    """
    # Arrange
    file_path = tmp_path / "invalid.parquet"
    file_path.write_text("not a parquet file")

    # Act & Assert
    with pytest.raises(Exception):  # noqa: B017 - pyarrow raises various exceptions
        get_parquet_schema(str(file_path))


def test_get_parquet_schema_returns_string_types(tmp_path: Path) -> None:
    """
    Test case 9: Test that schema values are strings.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"col": [1]})
    pq.write_table(table, file_path)

    # Act
    schema = get_parquet_schema(str(file_path))

    # Assert
    assert all(isinstance(v, str) for v in schema.values())
