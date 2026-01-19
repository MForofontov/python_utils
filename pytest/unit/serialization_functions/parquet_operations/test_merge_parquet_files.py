"""
Unit tests for merge_parquet_files function.
"""

import tempfile
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
from serialization_functions.parquet_operations.merge_parquet_files import (
    merge_parquet_files,
)

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.serialization]


def test_merge_parquet_files_basic() -> None:
    """
    Test basic merge of multiple Parquet files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "data1.parquet"
        file2 = Path(tmpdir) / "data2.parquet"
        output = Path(tmpdir) / "merged.parquet"

        # Create test data
        data1 = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        data2 = [{"id": 3, "name": "Charlie"}]

        table1 = pa.Table.from_pylist(data1)
        table2 = pa.Table.from_pylist(data2)

        pq.write_table(table1, file1)
        pq.write_table(table2, file2)

        rows = merge_parquet_files([file1, file2], output)

        assert rows == 3
        assert output.exists()

        # Verify merged data
        result = pq.read_table(output)
        assert len(result) == 3


def test_merge_parquet_files_three_files() -> None:
    """
    Test merging three files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        files = [Path(tmpdir) / f"data{i}.parquet" for i in range(3)]
        output = Path(tmpdir) / "merged.parquet"

        for idx, file_path in enumerate(files):
            data = [{"id": idx, "value": f"val{idx}"}]
            table = pa.Table.from_pylist(data)
            pq.write_table(table, file_path)

        rows = merge_parquet_files(files, output)

        assert rows == 3


def test_merge_parquet_files_custom_compression() -> None:
    """
    Test merging with custom compression.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "data1.parquet"
        file2 = Path(tmpdir) / "data2.parquet"
        output = Path(tmpdir) / "merged.parquet"

        data = [{"id": 1}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, file1)
        pq.write_table(table, file2)

        merge_parquet_files([file1, file2], output, compression="gzip")

        assert output.exists()


def test_merge_parquet_files_with_schema() -> None:
    """
    Test merging with explicit schema validation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "data1.parquet"
        file2 = Path(tmpdir) / "data2.parquet"
        output = Path(tmpdir) / "merged.parquet"

        schema = pa.schema([("id", pa.int64()), ("name", pa.string())])

        data1 = [{"id": 1, "name": "Alice"}]
        data2 = [{"id": 2, "name": "Bob"}]

        table1 = pa.Table.from_pylist(data1, schema=schema)
        table2 = pa.Table.from_pylist(data2, schema=schema)

        pq.write_table(table1, file1)
        pq.write_table(table2, file2)

        rows = merge_parquet_files([file1, file2], output, schema=schema)

        assert rows == 2


def test_merge_parquet_files_invalid_type_input_files() -> None:
    """
    Test TypeError for invalid input_files type.
    """
    with pytest.raises(TypeError, match="input_files must be a sequence"):
        merge_parquet_files("not_a_list", "output.parquet")  # type: ignore


def test_merge_parquet_files_invalid_compression() -> None:
    """
    Test ValueError for invalid compression codec.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "data1.parquet"
        output = Path(tmpdir) / "merged.parquet"

        data = [{"id": 1}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, file1)

        with pytest.raises(ValueError, match="compression must be one of"):
            merge_parquet_files([file1], output, compression="invalid")


def test_merge_parquet_files_empty_input_error() -> None:
    """
    Test ValueError for empty input list.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "merged.parquet"

        with pytest.raises(ValueError, match="input_files cannot be empty"):
            merge_parquet_files([], output)


def test_merge_parquet_files_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "merged.parquet"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            merge_parquet_files(["/nonexistent/file.parquet"], output)


def test_merge_parquet_files_schema_mismatch() -> None:
    """
    Test ValueError for schema mismatch.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "data1.parquet"
        file2 = Path(tmpdir) / "data2.parquet"
        output = Path(tmpdir) / "merged.parquet"

        data1 = [{"id": 1, "name": "Alice"}]
        data2 = [{"id": 2, "value": "Different"}]  # Different schema

        table1 = pa.Table.from_pylist(data1)
        table2 = pa.Table.from_pylist(data2)

        pq.write_table(table1, file1)
        pq.write_table(table2, file2)

        with pytest.raises(ValueError, match="Schema mismatch"):
            merge_parquet_files([file1, file2], output)
