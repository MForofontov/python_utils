"""
Parquet operations module.

Provides utilities for reading, writing, and querying Parquet files
using Apache Arrow. Parquet is a columnar storage format efficient
for analytics and large datasets.
"""

from .append_parquet import append_parquet
from .filter_parquet import filter_parquet
from .get_parquet_metadata import get_parquet_metadata
from .get_parquet_schema import get_parquet_schema
from .merge_parquet_files import merge_parquet_files
from .partition_parquet_by_column import partition_parquet_by_column
from .read_parquet import read_parquet
from .write_parquet import write_parquet

__all__ = [
    'append_parquet',
    'filter_parquet',
    'get_parquet_metadata',
    'get_parquet_schema',
    'merge_parquet_files',
    'partition_parquet_by_column',
    'read_parquet',
    'write_parquet',
]
