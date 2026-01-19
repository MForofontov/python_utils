"""Tests for stream_csv_chunks module."""

from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.serialization]
from python_utils.serialization_functions.csv_advanced.stream_csv_chunks import stream_csv_chunks


def test_stream_csv_chunks_basic(tmp_path: Path) -> None:
    """
    Test case 1: Test basic streaming of CSV in chunks.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    file_path.write_text("name,age\nAlice,30\nBob,25\nCharlie,35\n")

    # Act
    chunks = list(stream_csv_chunks(str(file_path), chunk_size=2))

    # Assert
    assert len(chunks) == 2  # 3 rows / 2 per chunk = 2 chunks
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1


def test_stream_csv_chunks_as_dicts(tmp_path: Path) -> None:
    """
    Test case 2: Test streaming as dictionaries.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    file_path.write_text("name,age\nAlice,30\n")

    # Act
    chunks = list(stream_csv_chunks(str(file_path), use_dict=True))

    # Assert
    assert len(chunks) == 1
    assert isinstance(chunks[0][0], dict)
    assert chunks[0][0]["name"] == "Alice"
    assert chunks[0][0]["age"] == "30"


def test_stream_csv_chunks_as_lists(tmp_path: Path) -> None:
    """
    Test case 3: Test streaming as lists.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    file_path.write_text("name,age\nAlice,30\n")

    # Act
    chunks = list(stream_csv_chunks(str(file_path), use_dict=False))

    # Assert
    assert len(chunks) == 1
    assert isinstance(chunks[0][0], list)
    assert chunks[0][0] == ["name", "age"]


def test_stream_csv_chunks_custom_chunk_size(tmp_path: Path) -> None:
    """
    Test case 4: Test with custom chunk size.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    rows = "name\n" + "\n".join([f"Row{i}" for i in range(10)])
    file_path.write_text(rows)

    # Act
    chunks = list(stream_csv_chunks(str(file_path), chunk_size=3))

    # Assert
    assert len(chunks) == 4  # 10 rows / 3 per chunk = 4 chunks (last partial)
    assert len(chunks[0]) == 3
    assert len(chunks[-1]) == 1


def test_stream_csv_chunks_large_file(tmp_path: Path) -> None:
    """
    Test case 5: Test streaming large file efficiently.
    """
    # Arrange
    file_path = tmp_path / "large.csv"
    rows = "value\n" + "\n".join([str(i) for i in range(1000)])
    file_path.write_text(rows)

    # Act
    total_rows = 0
    for chunk in stream_csv_chunks(str(file_path), chunk_size=100):
        total_rows += len(chunk)

    # Assert
    assert total_rows == 1000


def test_stream_csv_chunks_custom_encoding(tmp_path: Path) -> None:
    """
    Test case 6: Test with custom encoding.
    """
    # Arrange
    file_path = tmp_path / "encoded.csv"
    file_path.write_text("name\nAlice\n", encoding="utf-8")

    # Act
    chunks = list(stream_csv_chunks(str(file_path), encoding="utf-8"))

    # Assert
    assert len(chunks) == 1


def test_stream_csv_chunks_invalid_input_path_type_raises_error() -> None:
    """
    Test case 7: Test TypeError for invalid input_path type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="input_path must be a string"):
        list(stream_csv_chunks(123))


def test_stream_csv_chunks_invalid_chunk_size_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test TypeError for invalid chunk_size type.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    file_path.write_text("data\n")

    # Act & Assert
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        list(stream_csv_chunks(str(file_path), chunk_size="invalid"))


def test_stream_csv_chunks_invalid_chunk_size_value_raises_error(
    tmp_path: Path,
) -> None:
    """
    Test case 9: Test ValueError for non-positive chunk_size.
    """
    # Arrange
    file_path = tmp_path / "data.csv"
    file_path.write_text("data\n")

    # Act & Assert
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        list(stream_csv_chunks(str(file_path), chunk_size=0))


def test_stream_csv_chunks_nonexistent_file_raises_error(tmp_path: Path) -> None:
    """
    Test case 10: Test FileNotFoundError for non-existent file.
    """
    # Arrange
    nonexistent = tmp_path / "does_not_exist.csv"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        list(stream_csv_chunks(str(nonexistent)))


def test_stream_csv_chunks_empty_file(tmp_path: Path) -> None:
    """
    Test case 11: Test streaming empty CSV file.
    """
    # Arrange
    file_path = tmp_path / "empty.csv"
    file_path.write_text("")

    # Act
    chunks = list(stream_csv_chunks(str(file_path)))

    # Assert
    assert len(chunks) == 0


def test_stream_csv_chunks_with_delimiter_kwargs(tmp_path: Path) -> None:
    """
    Test case 12: Test passing additional csv reader kwargs.
    """
    # Arrange
    file_path = tmp_path / "pipe.csv"
    file_path.write_text("name|age\nAlice|30\n")

    # Act
    chunks = list(stream_csv_chunks(str(file_path), delimiter="|"))

    # Assert
    assert len(chunks) == 1
    assert chunks[0][0]["name"] == "Alice"
