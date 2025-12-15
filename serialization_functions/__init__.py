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
- CSV streaming for large files and custom dialect management
- Excel file operations with range handling and multi-sheet support
- Parquet operations with filtering, appending, and metadata extraction
- Avro schema validation with detailed error reporting
"""

from .avro_operations import (
    validate_avro_data,
)
from .csv_advanced import (
    register_csv_dialect,
    stream_csv_chunks,
)
from .excel_operations import (
    create_excel_workbook,
    get_sheet_names,
    read_excel_range,
    read_excel_sheet,
    write_excel_range,
    write_excel_sheet,
)
from .parquet_operations import (
    append_parquet,
    filter_parquet,
    get_parquet_metadata,
    get_parquet_schema,
    read_parquet,
    write_parquet,
)

__all__ = [
    # CSV advanced operations
    'register_csv_dialect',
    'stream_csv_chunks',
    
    # Excel operations
    'read_excel_sheet',
    'write_excel_sheet',
    'get_sheet_names',
    'create_excel_workbook',
    'read_excel_range',
    'write_excel_range',
    
    # Parquet operations
    'write_parquet',
    'read_parquet',
    'get_parquet_metadata',
    'get_parquet_schema',
    'append_parquet',
    'filter_parquet',
    
    # Avro operations
    'validate_avro_data',
]

__version__ = '1.0.0'
