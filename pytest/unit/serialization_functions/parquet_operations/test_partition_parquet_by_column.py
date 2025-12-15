"""
Unit tests for partition_parquet_by_column function.
"""

from pathlib import Path
import tempfile

import pytest
import pyarrow as pa
import pyarrow.parquet as pq
from serialization_functions.parquet_operations.partition_parquet_by_column import partition_parquet_by_column


def test_partition_parquet_by_column_basic() -> None:
    """
    Test basic partitioning by column.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [
            {'id': 1, 'category': 'A', 'value': 100},
            {'id': 2, 'category': 'B', 'value': 200},
            {'id': 3, 'category': 'A', 'value': 150},
            {'id': 4, 'category': 'C', 'value': 300},
        ]
        
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        counts = partition_parquet_by_column(input_file, output_dir, 'category')
        
        assert len(counts) == 3
        assert counts['A'] == 2
        assert counts['B'] == 1
        assert counts['C'] == 1
        
        # Verify partition files
        assert (output_dir / "A.parquet").exists()
        assert (output_dir / "B.parquet").exists()
        assert (output_dir / "C.parquet").exists()


def test_partition_parquet_by_column_custom_compression() -> None:
    """
    Test partitioning with custom compression.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [{'id': 1, 'type': 'X'}, {'id': 2, 'type': 'Y'}]
        
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        counts = partition_parquet_by_column(
            input_file,
            output_dir,
            'type',
            compression='gzip'
        )
        
        assert len(counts) == 2


def test_partition_parquet_by_column_numeric_values() -> None:
    """
    Test partitioning by numeric column values.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [
            {'id': 1, 'year': 2020},
            {'id': 2, 'year': 2021},
            {'id': 3, 'year': 2020},
        ]
        
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        counts = partition_parquet_by_column(input_file, output_dir, 'year')
        
        assert counts[2020] == 2
        assert counts[2021] == 1


def test_partition_parquet_by_column_creates_output_dir() -> None:
    """
    Test that output directory is created if it doesn't exist.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "new" / "partitioned"
        
        data = [{'id': 1, 'cat': 'A'}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        partition_parquet_by_column(input_file, output_dir, 'cat')
        
        assert output_dir.exists()


def test_partition_parquet_by_column_safe_filenames() -> None:
    """
    Test that special characters in values are handled in filenames.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [
            {'id': 1, 'path': '/usr/local'},
            {'id': 2, 'path': 'C:\\Windows'},
        ]
        
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        counts = partition_parquet_by_column(input_file, output_dir, 'path')
        
        # Check that files were created with safe names
        files = list(output_dir.glob("*.parquet"))
        assert len(files) == 2


def test_partition_parquet_by_column_invalid_type_input() -> None:
    """
    Test TypeError for invalid input_file type.
    """
    with pytest.raises(TypeError, match="input_file must be str or Path"):
        partition_parquet_by_column(123, "output", "column")  # type: ignore


def test_partition_parquet_by_column_invalid_compression() -> None:
    """
    Test ValueError for invalid compression codec.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [{'id': 1, 'cat': 'A'}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        with pytest.raises(ValueError, match="compression must be one of"):
            partition_parquet_by_column(input_file, output_dir, 'cat', compression='invalid')


def test_partition_parquet_by_column_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "partitioned"
        
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            partition_parquet_by_column("/nonexistent/file.parquet", output_dir, "column")


def test_partition_parquet_by_column_invalid_column() -> None:
    """
    Test ValueError for non-existent partition column.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [{'id': 1, 'name': 'Alice'}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        with pytest.raises(ValueError, match="Partition column .* not found"):
            partition_parquet_by_column(input_file, output_dir, 'nonexistent')


def test_partition_parquet_by_column_exceeds_max_partitions() -> None:
    """
    Test ValueError when exceeding max_partitions limit.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "data.parquet"
        output_dir = Path(tmpdir) / "partitioned"
        
        data = [{'id': i, 'cat': f'cat{i}'} for i in range(10)]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, input_file)
        
        with pytest.raises(ValueError, match="exceeds max_partitions"):
            partition_parquet_by_column(input_file, output_dir, 'cat', max_partitions=5)
