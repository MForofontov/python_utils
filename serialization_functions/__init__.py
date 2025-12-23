"""
Serialization functions module.

Provides utilities for advanced data serialization that add value beyond
simple library wrappers. Focuses on complex operations that require logic,
validation, or transformation.

This module complements existing serialization in the codebase:
- json_functions/ handles JSON operations
- env_config_functions/ handles YAML and TOML configuration files
- file_functions/data_format_operations/ handles basic CSV/TSV operations

The serialization_functions module adds:
- CSV advanced: streaming, merging, validation, column transformations
- Excel operations: range handling, multi-sheet merging, transposing, auto-formatting
- Parquet operations: filtering, merging, partitioning, metadata extraction
- Format converters: CSV ↔ Parquet ↔ Excel with transformations
"""

from .csv_advanced import (
    merge_csv_files,
    register_csv_dialect,
    stream_csv_chunks,
    transform_csv_columns,
    validate_csv_structure,
)
from .excel_operations import (
    auto_format_excel_columns,
    create_excel_workbook,
    get_sheet_names,
    merge_excel_sheets,
    read_excel_range,
    read_excel_sheet,
    transpose_excel_data,
    validate_excel_structure,
    write_excel_range,
    write_excel_sheet,
)
from .format_converters import (
    csv_to_parquet,
    excel_to_csv_batch,
    excel_to_parquet,
    parquet_to_csv,
    parquet_to_excel,
)
from .parquet_operations import (
    append_parquet,
    filter_parquet,
    get_parquet_metadata,
    get_parquet_schema,
    merge_parquet_files,
    partition_parquet_by_column,
    read_parquet,
    write_parquet,
)

__all__ = [
    # CSV advanced operations
    'merge_csv_files',
    'register_csv_dialect',
    'stream_csv_chunks',
    'transform_csv_columns',
    'validate_csv_structure',
    
    # Excel operations
    'auto_format_excel_columns',
    'create_excel_workbook',
    'get_sheet_names',
    'merge_excel_sheets',
    'read_excel_range',
    'read_excel_sheet',
    'transpose_excel_data',
    'validate_excel_structure',
    'write_excel_range',
    'write_excel_sheet',
    
    # Parquet operations
    'append_parquet',
    'filter_parquet',
    'get_parquet_metadata',
    'get_parquet_schema',
    'merge_parquet_files',
    'partition_parquet_by_column',
    'read_parquet',
    'write_parquet',
    
    # Format converters
    'csv_to_parquet',
    'excel_to_csv_batch',
    'excel_to_parquet',
    'parquet_to_csv',
    'parquet_to_excel',
]

from .._version import __version__
