"""
Convert CSV to Parquet with schema inference and transformations.
"""

import csv
from pathlib import Path
from typing import Any, Callable

import pyarrow as pa
import pyarrow.parquet as pq


def csv_to_parquet(
    input_file: str | Path,
    output_file: str | Path,
    *,
    schema: pa.Schema | None = None,
    type_inference: bool = True,
    transformers: dict[str, Callable[[str], Any]] | None = None,
    chunk_size: int = 10000,
    compression: str = "snappy",
    encoding: str = 'utf-8',
    **csv_kwargs: Any,
) -> int:
    """
    Convert CSV file to Parquet format with schema inference and transformations.

    Provides efficient CSV to Parquet conversion with automatic type detection,
    custom transformations, and chunked processing for large files.

    Parameters
    ----------
    input_file : str | Path
        Path to input CSV file.
    output_file : str | Path
        Path to output Parquet file.
    schema : pa.Schema | None, optional
        PyArrow schema to use (by default None for auto-inference).
    type_inference : bool, optional
        Auto-infer column types from data (by default True).
    transformers : dict[str, Callable[[str], Any]] | None, optional
        Functions to transform column values during conversion (by default None).
    chunk_size : int, optional
        Number of rows to process at once (by default 10000).
    compression : str, optional
        Compression codec: 'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'none'
        (by default 'snappy').
    encoding : str, optional
        CSV file encoding (by default 'utf-8').
    **csv_kwargs : Any
        Additional arguments for csv.DictReader.

    Returns
    -------
    int
        Number of rows written to Parquet file.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If input file doesn't exist.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> # Basic conversion
    >>> rows = csv_to_parquet('data.csv', 'data.parquet')
    >>> rows
    10000

    >>> # With custom transformers
    >>> transformers = {
    ...     'age': int,
    ...     'salary': float,
    ...     'email': str.lower
    ... }
    >>> csv_to_parquet('data.csv', 'data.parquet', transformers=transformers)
    10000

    >>> # With explicit schema
    >>> import pyarrow as pa
    >>> schema = pa.schema([
    ...     ('id', pa.int64()),
    ...     ('name', pa.string()),
    ...     ('age', pa.int32())
    ... ])
    >>> csv_to_parquet('data.csv', 'data.parquet', schema=schema)
    10000

    Notes
    -----
    Type inference samples first chunk to determine column types.
    Transformers are applied before type inference.
    Parquet format is highly efficient for analytics and cloud storage.

    Complexity
    ----------
    Time: O(n) where n=number of rows
    Space: O(c) where c=chunk_size
    """
    # Type validation
    if not isinstance(input_file, (str, Path)):
        raise TypeError(
            f"input_file must be str or Path, got {type(input_file).__name__}"
        )
    if not isinstance(output_file, (str, Path)):
        raise TypeError(
            f"output_file must be str or Path, got {type(output_file).__name__}"
        )
    if schema is not None and not isinstance(schema, pa.Schema):
        raise TypeError(
            f"schema must be pa.Schema or None, got {type(schema).__name__}"
        )
    if not isinstance(type_inference, bool):
        raise TypeError(
            f"type_inference must be bool, got {type(type_inference).__name__}"
        )
    if transformers is not None and not isinstance(transformers, dict):
        raise TypeError(
            f"transformers must be dict or None, got {type(transformers).__name__}"
        )
    if not isinstance(chunk_size, int):
        raise TypeError(f"chunk_size must be int, got {type(chunk_size).__name__}")
    if not isinstance(compression, str):
        raise TypeError(f"compression must be str, got {type(compression).__name__}")
    if not isinstance(encoding, str):
        raise TypeError(f"encoding must be str, got {type(encoding).__name__}")

    # Value validation
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    valid_compressions = {'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'none'}
    if compression not in valid_compressions:
        raise ValueError(
            f"compression must be one of {valid_compressions}, got '{compression}'"
        )

    # Read CSV and convert to Parquet
    total_rows = 0
    writer = None
    inferred_schema = schema

    try:
        with open(input_file, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile, **csv_kwargs)

            if reader.fieldnames is None:
                raise ValueError("CSV file has no header")

            fieldnames = list(reader.fieldnames)
            chunk: list[dict[str, Any]] = []

            for row in reader:
                # Apply transformers
                if transformers:
                    for col, transformer in transformers.items():
                        if col in row:
                            try:
                                row[col] = transformer(row[col])
                            except Exception as e:
                                raise ValueError(
                                    f"Error transforming column '{col}' at row {total_rows + 1}: {e}"
                                ) from e

                chunk.append(row)

                # Process chunk when size reached
                if len(chunk) >= chunk_size:
                    # Convert chunk to PyArrow table
                    if inferred_schema is None and type_inference:
                        # Infer schema from first chunk
                        table = pa.Table.from_pylist(chunk)
                        inferred_schema = table.schema
                    elif inferred_schema is not None:
                        table = pa.Table.from_pylist(chunk, schema=inferred_schema)
                    else:
                        # No inference, all columns as strings
                        table = pa.Table.from_pylist(chunk)

                    # Write to Parquet
                    if writer is None:
                        writer = pq.ParquetWriter(
                            output_file,
                            table.schema,
                            compression=compression
                        )

                    writer.write_table(table)
                    total_rows += len(chunk)
                    chunk = []

            # Process remaining rows
            if chunk:
                if inferred_schema is None and type_inference:
                    table = pa.Table.from_pylist(chunk)
                    inferred_schema = table.schema
                elif inferred_schema is not None:
                    table = pa.Table.from_pylist(chunk, schema=inferred_schema)
                else:
                    table = pa.Table.from_pylist(chunk)

                if writer is None:
                    writer = pq.ParquetWriter(
                        output_file,
                        table.schema,
                        compression=compression
                    )

                writer.write_table(table)
                total_rows += len(chunk)

    finally:
        if writer is not None:
            writer.close()

    return total_rows


__all__ = ['csv_to_parquet']
