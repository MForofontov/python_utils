"""
Partition Parquet data into multiple files by column values.
"""

from pathlib import Path
from typing import Any
from collections.abc import Sequence

import pyarrow as pa
import pyarrow.parquet as pq


def partition_parquet_by_column(
    input_file: str | Path,
    output_dir: str | Path,
    partition_column: str,
    *,
    compression: str = "snappy",
    max_partitions: int | None = None,
) -> dict[Any, int]:
    """
    Partition Parquet file into multiple files based on column values.

    Splits a single Parquet file into multiple files, one per unique value
    in the partition column. Useful for organizing large datasets by category.

    Parameters
    ----------
    input_file : str | Path
        Path to input Parquet file.
    output_dir : str | Path
        Directory for output partitioned files.
    partition_column : str
        Column name to partition by.
    compression : str, optional
        Compression codec: 'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'none'
        (by default 'snappy').
    max_partitions : int | None, optional
        Maximum number of partitions (by default None for unlimited).

    Returns
    -------
    dict[Any, int]
        Mapping of partition value to row count for each partition.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    FileNotFoundError
        If input file doesn't exist.
    ValueError
        If partition_column doesn't exist or max_partitions exceeded.

    Examples
    --------
    >>> # Partition by category
    >>> counts = partition_parquet_by_column(
    ...     'data.parquet',
    ...     'partitioned/',
    ...     'category'
    ... )
    >>> counts
    {'electronics': 500, 'clothing': 300, 'food': 200}

    >>> # Partition by date with limit
    >>> partition_parquet_by_column(
    ...     'logs.parquet',
    ...     'logs_by_date/',
    ...     'date',
    ...     max_partitions=31
    ... )
    {'2024-01-01': 1000, '2024-01-02': 1200, ...}

    Notes
    -----
    Output files are named: {partition_value}.parquet
    Creates output_dir if it doesn't exist.
    Efficient for organizing data by categorical or temporal dimensions.

    Complexity
    ----------
    Time: O(n*log(k)) where n=rows, k=unique partition values
    Space: O(k*b) where k=partitions, b=batch size
    """
    # Type validation
    if not isinstance(input_file, (str, Path)):
        raise TypeError(
            f"input_file must be str or Path, got {type(input_file).__name__}"
        )
    if not isinstance(output_dir, (str, Path)):
        raise TypeError(
            f"output_dir must be str or Path, got {type(output_dir).__name__}"
        )
    if not isinstance(partition_column, str):
        raise TypeError(
            f"partition_column must be str, got {type(partition_column).__name__}"
        )
    if not isinstance(compression, str):
        raise TypeError(f"compression must be str, got {type(compression).__name__}")
    if max_partitions is not None and not isinstance(max_partitions, int):
        raise TypeError(
            f"max_partitions must be int or None, got {type(max_partitions).__name__}"
        )

    # Value validation
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not partition_column:
        raise ValueError("partition_column cannot be empty")

    valid_compressions = {'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'none'}
    if compression not in valid_compressions:
        raise ValueError(
            f"compression must be one of {valid_compressions}, got '{compression}'"
        )
    if max_partitions is not None and max_partitions <= 0:
        raise ValueError(f"max_partitions must be positive, got {max_partitions}")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read input file
    table = pq.read_table(input_file)

    # Validate partition column exists
    if partition_column not in table.schema.names:
        raise ValueError(
            f"Partition column '{partition_column}' not found in schema. "
            f"Available columns: {table.schema.names}"
        )

    # Get unique partition values
    partition_values = table.column(partition_column).unique().to_pylist()

    # Check max partitions limit
    if max_partitions is not None and len(partition_values) > max_partitions:
        raise ValueError(
            f"Number of unique values ({len(partition_values)}) exceeds "
            f"max_partitions ({max_partitions})"
        )

    # Partition data and write files
    partition_counts: dict[Any, int] = {}

    for value in partition_values:
        # Filter rows for this partition
        mask = pa.compute.equal(table.column(partition_column), value)
        partition_table = table.filter(mask)

        # Generate safe filename from partition value
        safe_value = str(value).replace('/', '_').replace('\\', '_').replace(' ', '_')
        output_file_path = output_path / f"{safe_value}.parquet"

        # Write partition file
        pq.write_table(
            partition_table,
            output_file_path,
            compression=compression
        )

        partition_counts[value] = len(partition_table)

    return partition_counts


__all__ = ['partition_parquet_by_column']
