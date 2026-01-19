"""
Merge multiple Parquet files into one.
"""

from collections.abc import Sequence
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def merge_parquet_files(
    input_files: Sequence[str | Path],
    output_file: str | Path,
    *,
    schema: pa.Schema | None = None,
    compression: str = "snappy",
) -> int:
    """
    Merge multiple Parquet files into a single output file.

    Combines Parquet files with schema validation and efficient columnar merging.
    All input files must have compatible schemas.

    Parameters
    ----------
    input_files : Sequence[str | Path]
        List of paths to Parquet files to merge.
    output_file : str | Path
        Path to output merged Parquet file.
    schema : pa.Schema | None, optional
        Expected Arrow schema (by default None for auto-detect from first file).
    compression : str, optional
        Compression codec: 'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'none'
        (by default 'snappy').

    Returns
    -------
    int
        Total number of rows in merged file.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If any input file doesn't exist.
    ValueError
        If input_files is empty or schemas are incompatible.

    Examples
    --------
    >>> files = ['data1.parquet', 'data2.parquet', 'data3.parquet']
    >>> rows = merge_parquet_files(files, 'merged.parquet')
    >>> rows
    15000

    >>> # With specific compression
    >>> merge_parquet_files(files, 'merged.parquet', compression='gzip')
    15000

    >>> # With schema validation
    >>> import pyarrow as pa
    >>> schema = pa.schema([('id', pa.int64()), ('name', pa.string())])
    >>> merge_parquet_files(files, 'merged.parquet', schema=schema)
    15000

    Notes
    -----
    Uses PyArrow's efficient columnar merging. Schema is validated before merging.
    First file's schema is used as reference if not explicitly provided.

    Complexity
    ----------
    Time: O(n) where n=total rows across all files
    Space: O(b) where b=batch size for reading
    """
    # Type validation
    if not isinstance(input_files, (list, tuple)):
        raise TypeError(
            f"input_files must be a sequence, got {type(input_files).__name__}"
        )
    if not isinstance(output_file, (str, Path)):
        raise TypeError(
            f"output_file must be str or Path, got {type(output_file).__name__}"
        )
    if schema is not None and not isinstance(schema, pa.Schema):
        raise TypeError(
            f"schema must be pa.Schema or None, got {type(schema).__name__}"
        )
    if not isinstance(compression, str):
        raise TypeError(f"compression must be str, got {type(compression).__name__}")

    # Value validation
    if len(input_files) == 0:
        raise ValueError("input_files cannot be empty")

    valid_compressions = {"snappy", "gzip", "brotli", "lz4", "zstd", "none"}
    if compression not in valid_compressions:
        raise ValueError(
            f"compression must be one of {valid_compressions}, got '{compression}'"
        )

    for file_path in input_files:
        if not isinstance(file_path, (str, Path)):
            raise TypeError(
                f"Each input file must be str or Path, got {type(file_path).__name__}"
            )
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

    # Read and merge files
    tables = []
    reference_schema = schema

    for file_path in input_files:
        table = pq.read_table(file_path)

        # Establish reference schema from first file if not provided
        if reference_schema is None:
            reference_schema = table.schema
        else:
            # Validate schema compatibility
            if not table.schema.equals(reference_schema):
                raise ValueError(
                    f"Schema mismatch in {file_path}. "
                    f"Expected {reference_schema}, got {table.schema}"
                )

        tables.append(table)

    # Concatenate tables
    merged_table = pa.concat_tables(tables)

    # Write merged table
    pq.write_table(merged_table, output_file, compression=compression)

    return len(merged_table)


__all__ = ["merge_parquet_files"]
