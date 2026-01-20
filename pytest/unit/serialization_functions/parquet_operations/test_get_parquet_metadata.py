"""Tests for get_parquet_metadata module."""

from pathlib import Path

import pytest

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    from python_utils.serialization_functions.parquet_operations.get_parquet_metadata import (
        get_parquet_metadata,
    )
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    pa = None  # type: ignore
    pq = None  # type: ignore
    get_parquet_metadata = None  # type: ignore

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.serialization]


def test_get_parquet_metadata_basic(tmp_path: Path) -> None:
    """
    Test case 1: Test getting basic metadata from Parquet file.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice", "Bob"], "age": [30, 25]})
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert metadata["num_rows"] == 2
    assert metadata["num_columns"] == 2
    assert set(metadata["columns"]) == {"name", "age"}


def test_get_parquet_metadata_single_row(tmp_path: Path) -> None:
    """
    Test case 2: Test metadata for single row file.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"value": [1]})
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert metadata["num_rows"] == 1
    assert metadata["num_columns"] == 1


def test_get_parquet_metadata_many_columns(tmp_path: Path) -> None:
    """
    Test case 3: Test metadata for file with many columns.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    data = {f"col{i}": [i] for i in range(10)}
    table = pa.table(data)
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert metadata["num_columns"] == 10
    assert len(metadata["columns"]) == 10


def test_get_parquet_metadata_includes_schema(tmp_path: Path) -> None:
    """
    Test case 4: Test that metadata includes schema information.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"name": ["Alice"]})
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert "schema" in metadata
    assert isinstance(metadata["schema"], str)
    assert "name" in metadata["schema"]


def test_get_parquet_metadata_includes_row_groups(tmp_path: Path) -> None:
    """
    Test case 5: Test that metadata includes row group count.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"value": [1, 2, 3]})
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert "num_row_groups" in metadata
    assert metadata["num_row_groups"] >= 1


def test_get_parquet_metadata_invalid_file_path_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid file_path type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        get_parquet_metadata(123)


def test_get_parquet_metadata_nonexistent_file_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test error for non-existent file.
    """
    # Arrange
    nonexistent = tmp_path / "does_not_exist.parquet"

    # Act & Assert
    with pytest.raises(Exception):  # noqa: B017 - pyarrow raises various exceptions
        get_parquet_metadata(str(nonexistent))


def test_get_parquet_metadata_invalid_file_format_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test error for invalid Parquet file.
    """
    # Arrange
    file_path = tmp_path / "invalid.parquet"
    file_path.write_text("not a parquet file")

    # Act & Assert
    with pytest.raises(Exception):  # noqa: B017 - pyarrow raises various exceptions
        get_parquet_metadata(str(file_path))


def test_get_parquet_metadata_includes_serialized_size(tmp_path: Path) -> None:
    """
    Test case 9: Test that metadata includes serialized size.
    """
    # Arrange

    file_path = tmp_path / "data.parquet"
    table = pa.table({"data": [1, 2, 3]})
    pq.write_table(table, file_path)

    # Act
    metadata = get_parquet_metadata(str(file_path))

    # Assert
    assert "serialized_size" in metadata
    assert metadata["serialized_size"] > 0
