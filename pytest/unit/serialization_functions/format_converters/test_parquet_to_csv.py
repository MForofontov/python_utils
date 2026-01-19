"""
Unit tests for parquet_to_csv function.
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
from serialization_functions.format_converters.parquet_to_csv import parquet_to_csv

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")


def test_parquet_to_csv_basic() -> None:
    """
    Test basic Parquet to CSV conversion.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        rows = parquet_to_csv(parquet_file, csv_file)

        assert rows == 2
        assert csv_file.exists()

        # Verify CSV content
        with open(csv_file) as f:
            lines = f.readlines()
            assert len(lines) == 3  # header + 2 rows
            assert "id,name,age" in lines[0]


def test_parquet_to_csv_select_columns() -> None:
    """
    Test selecting specific columns.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        rows = parquet_to_csv(parquet_file, csv_file, columns=["id", "name"])

        assert rows == 1

        with open(csv_file) as f:
            header = f.readline()
            assert "id,name" in header
            assert "email" not in header


def test_parquet_to_csv_max_rows() -> None:
    """
    Test limiting maximum rows.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": i} for i in range(100)]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        rows = parquet_to_csv(parquet_file, csv_file, max_rows=10)

        assert rows == 10


def test_parquet_to_csv_filter_rows() -> None:
    """
    Test filtering rows with custom function.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": i, "value": i * 10} for i in range(10)]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        # Filter rows where value > 50
        rows = parquet_to_csv(
            parquet_file, csv_file, filter_func=lambda row: row["value"] > 50
        )

        assert rows == 4  # ids 6, 7, 8, 9


def test_parquet_to_csv_no_header() -> None:
    """
    Test without header row.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": 1, "name": "Alice"}]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        parquet_to_csv(parquet_file, csv_file, include_header=False)

        with open(csv_file) as f:
            lines = f.readlines()
            assert len(lines) == 1  # only data row, no header
            assert "id" not in lines[0]


def test_parquet_to_csv_custom_delimiter() -> None:
    """
    Test custom delimiter (TSV).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        tsv_file = Path(tmpdir) / "output.tsv"

        data = [{"col1": "a", "col2": "b"}]

        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        parquet_to_csv(parquet_file, tsv_file, delimiter="\t")

        with open(tsv_file) as f:
            header = f.readline()
            assert "\t" in header
            assert "," not in header


def test_parquet_to_csv_empty_data() -> None:
    """
    Test handling empty Parquet file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data: list[dict] = []
        schema = pa.schema([("id", pa.int64())])
        table = pa.Table.from_pylist(data, schema=schema)
        pq.write_table(table, parquet_file)

        rows = parquet_to_csv(parquet_file, csv_file)

        assert rows == 0


def test_parquet_to_csv_invalid_type_input() -> None:
    """
    Test TypeError for invalid input_file type.
    """
    with pytest.raises(TypeError, match="input_file must be str or Path"):
        parquet_to_csv(123, "output.csv")  # type: ignore


def test_parquet_to_csv_invalid_max_rows() -> None:
    """
    Test ValueError for invalid max_rows.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": 1}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        with pytest.raises(ValueError, match="max_rows must be positive"):
            parquet_to_csv(parquet_file, csv_file, max_rows=0)


def test_parquet_to_csv_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "output.csv"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            parquet_to_csv("/nonexistent/file.parquet", csv_file)


def test_parquet_to_csv_invalid_delimiter() -> None:
    """
    Test ValueError for multi-character delimiter.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": 1}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        with pytest.raises(ValueError, match="delimiter must be single character"):
            parquet_to_csv(parquet_file, csv_file, delimiter="||")


def test_parquet_to_csv_invalid_column() -> None:
    """
    Test ValueError for non-existent column.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file = Path(tmpdir) / "output.csv"

        data = [{"id": 1, "name": "Alice"}]
        table = pa.Table.from_pylist(data)
        pq.write_table(table, parquet_file)

        # PyArrow raises ArrowInvalid for invalid columns
        with pytest.raises(Exception, match="(No match for|not found)"):
            parquet_to_csv(parquet_file, csv_file, columns=["nonexistent"])
