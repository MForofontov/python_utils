"""
Unit tests for csv_to_parquet function.
"""

import csv
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
from serialization_functions.format_converters.csv_to_parquet import csv_to_parquet

pytestmark = pytest.mark.skipif(not PYARROW_AVAILABLE, reason="pyarrow not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.serialization]


def test_csv_to_parquet_basic() -> None:
    """
    Test basic CSV to Parquet conversion.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age"])
            writer.writerow(["1", "Alice", "30"])
            writer.writerow(["2", "Bob", "25"])

        rows = csv_to_parquet(csv_file, parquet_file)

        assert rows == 2
        assert parquet_file.exists()

        # Verify Parquet data
        table = pq.read_table(parquet_file)
        assert len(table) == 2


def test_csv_to_parquet_with_transformers() -> None:
    """
    Test CSV to Parquet with value transformers.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "age", "email"])
            writer.writerow(["1", "30", "ALICE@EXAMPLE.COM"])

        transformers = {"id": int, "age": int, "email": str.lower}

        rows = csv_to_parquet(csv_file, parquet_file, transformers=transformers)

        assert rows == 1

        table = pq.read_table(parquet_file)
        data = table.to_pylist()
        assert data[0]["email"] == "alice@example.com"


def test_csv_to_parquet_custom_compression() -> None:
    """
    Test CSV to Parquet with custom compression.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id"])
            writer.writerow(["1"])

        csv_to_parquet(csv_file, parquet_file, compression="gzip")

        assert parquet_file.exists()


def test_csv_to_parquet_with_schema() -> None:
    """
    Test CSV to Parquet with explicit schema.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name"])
            writer.writerow(["1", "Alice"])

        schema = pa.schema([("id", pa.int64()), ("name", pa.string())])

        transformers = {"id": int}
        csv_to_parquet(csv_file, parquet_file, schema=schema, transformers=transformers)

        table = pq.read_table(parquet_file)
        assert table.schema.equals(schema)


def test_csv_to_parquet_large_file_chunking() -> None:
    """
    Test chunked processing for large files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "value"])
            for i in range(100):
                writer.writerow([str(i), f"value{i}"])

        rows = csv_to_parquet(csv_file, parquet_file, chunk_size=25)

        assert rows == 100


def test_csv_to_parquet_no_type_inference() -> None:
    """
    Test without type inference (all strings).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "value"])
            writer.writerow(["1", "100"])

        csv_to_parquet(csv_file, parquet_file, type_inference=False)

        table = pq.read_table(parquet_file)
        assert table.schema.field("id").type == pa.string()


def test_csv_to_parquet_invalid_type_input() -> None:
    """
    Test TypeError for invalid input_file type.
    """
    with pytest.raises(TypeError, match="input_file must be str or Path"):
        csv_to_parquet(123, "output.parquet")  # type: ignore


def test_csv_to_parquet_invalid_chunk_size() -> None:
    """
    Test ValueError for invalid chunk_size.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"
        csv_file.touch()

        with pytest.raises(ValueError, match="chunk_size must be positive"):
            csv_to_parquet(csv_file, parquet_file, chunk_size=0)


def test_csv_to_parquet_file_not_found() -> None:
    """
    Test FileNotFoundError for non-existent file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "output.parquet"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            csv_to_parquet("/nonexistent/file.csv", parquet_file)


def test_csv_to_parquet_invalid_compression() -> None:
    """
    Test ValueError for invalid compression codec.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "data.csv"
        parquet_file = Path(tmpdir) / "data.parquet"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id"])
            writer.writerow(["1"])

        with pytest.raises(ValueError, match="compression must be one of"):
            csv_to_parquet(csv_file, parquet_file, compression="invalid")
