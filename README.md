# Python Utilities

A comprehensive collection of 400+ reusable Python utilities and functions covering a wide range of programming tasks. This library provides modular, well-tested, and documented functions organized by domain to help accelerate development across various Python projects.

## 🚀 Overview

This repository contains over **400+ utility functions, classes, and decorators** organized into **24 specialized modules**. Each module focuses on a specific domain and provides production-ready implementations with comprehensive documentation, type hints, and unit tests.

**Key Highlights:**
- 🎯 **24+ specialized modules** covering asyncio, databases, files, networking, and more
- 📝 **NumPy-style docstrings** with examples and complexity analysis
- 🔒 **Complete type hints** for all functions (Python 3.10+)
- ✅ **88%+ test coverage** with comprehensive unit tests
- 🐍 **Modern Python** practices (3.10+)
- 📦 **Modular design** - use only what you need

## 📦 Installation

### From GitHub
```bash
pip install git+https://github.com/MForofontov/python-utils.git
```

### Development Installation
```bash
git clone https://github.com/MForofontov/python-utils.git
cd python-utils
pip install -e ".[dev]"
```

## 🗂️ Module Structure

### 🔄 Asyncio Functions (`asyncio_functions/`)
**17 functions** for advanced asynchronous programming:

- **Task Management**: `async_batch`, `async_chain`, `async_throttle`, `async_cancellable_task`
- **Error Handling**: `async_await_with_error_handling`, `retry_async`, `async_retry_with_backoff`
- **Resource Management**: `AsyncConnectionPool`, `async_cleanup`
- **Rate Limiting**: `async_rate_limited`, `async_periodic`
- **HTTP Utilities**: `fetch_url`, `fetch_multiple_urls`, `async_download`, `async_parallel_download`
- **Stream Processing**: `async_stream_processor`
- **Utilities**: `gather_with_timeout`, `async_event_loop`

### 🗜️ Compression Functions (`compression_functions/`)
**27 functions** for data compression supporting multiple algorithms:

#### Binary Compression
- **Algorithms**: GZIP, BZ2, LZMA, Zlib, Snappy, Zstandard
- **Functions**: `compress_data`, `decompress_data` with auto-format detection

#### File Compression
- **Archive Formats**: ZIP, TAR (with GZIP/BZ2/LZMA compression)
- **Batch Processing**: Handle multiple files and directories

#### Specialized Compression
- **Polyline Encoding**: Efficient list-of-integers compression
- **Number Compression**: Numerical data optimization

### 🗄️ Database Functions (`database_functions/`)
**23 functions** for database operations with SQLAlchemy support:

#### Connection Management
- `create_connection`: Universal connection factory (PostgreSQL, MySQL, SQLite, Oracle, SQL Server)
- `get_connection_pool`: Connection pooling with configurable sizes
- `test_connection`: Connection health checks

#### Transaction Management
- `atomic_transaction`: ACID-compliant transactions with automatic rollback
- `nested_transaction`: Savepoint-based nested transactions
- `transaction_context`: Context manager for transaction control

#### Query Execution
- `execute_query`: Safe parameterized query execution
- `execute_many`: Batch query execution
- `fetch_one`, `fetch_all`: Result fetching utilities

#### Bulk Operations
- `execute_bulk_chunked`: Memory-efficient bulk inserts
- `batch_insert`: High-performance batch insertion
- `bulk_update`: Optimized bulk updates

#### Schema Inspection (**15 utilities**)
- `get_table_info`: Comprehensive table metadata
- `compare_schemas`: Cross-database schema comparison
- `detect_schema_drift`: Validate actual vs expected schema
- `get_foreign_key_dependencies`: Topological sorting for safe operations
- `verify_referential_integrity`: Find orphaned records
- `get_column_statistics`: Data profiling and quality metrics
- `find_duplicate_indexes`: Performance optimization analysis
- `safe_truncate_tables`: FK-aware table truncation
- `find_duplicate_rows`: Duplicate detection
- `get_table_sizes`: Storage analysis (PostgreSQL, MySQL, SQLite, Oracle, SQL Server)
- `check_encoding_issues`: Text encoding validation
- `find_unused_columns`: Identify rarely-used columns
- `find_missing_indexes`: Index recommendations
- `compare_table_data`: Migration validation
- `check_data_anomalies`: Data quality monitoring

### 📅 Datetime Functions (`datetime_functions/`)
**27 functions** for date and time manipulation:

- **Conversion**: `convert_to_utc`, `convert_timezone`, `parse_iso8601`
- **Calculations**: `add_business_days`, `get_age`, `time_until`
- **Formatting**: `format_relative_time`, `humanize_duration`
- **Business Logic**: `is_business_day`, `get_next_business_day`
- **Range Operations**: `generate_date_range`, `split_date_range`

### 🎨 Decorators (`decorators/`)
**50+ decorators** for function enhancement:

#### Performance & Monitoring
- `@time_function`: Execution time measurement with statistics
- `@time_and_resource_function`: CPU, memory, and time profiling
- `@cache`: LRU caching with TTL support
- `@cache_with_expiration`: Time-based cache invalidation

#### Error Handling & Resilience
- `@handle_error`: Comprehensive error handling with logging
- `@retry`: Configurable retry with exponential backoff
- `@timeout`: Function execution timeouts
- `@circuit_breaker`: Circuit breaker pattern for fault tolerance

#### Input/Output Processing
- `@enforce_types`: Runtime type checking
- `@validate_args`: Argument validation with custom rules
- `@normalize_input`: Input data normalization
- `@format_output`: Output formatting and transformation

#### Control Flow
- `@rate_limit`: Function call rate limiting
- `@throttle`: Request throttling
- `@deprecated`: Deprecation warnings with migration hints

### 📁 File Functions (`file_functions/`)
**32 functions** organized into specialized submodules:

#### File Operations
- `read_file_lines`, `write_file_lines`: Line-based I/O
- `append_to_file`, `copy_file`, `move_file`
- `get_file_size`, `file_exists`, `ensure_file_exists`

#### Directory Operations
- `create_directory`, `delete_directory`, `list_files`
- `copy_directory`, `move_directory`

#### Path Operations
- `normalize_path`, `get_absolute_path`, `get_relative_path`
- `split_path`, `join_paths`

#### File Hashing
- `hash_file`: Support for MD5, SHA1, SHA256, SHA512
- `verify_file_hash`: Integrity checking

#### Data Format Operations
- `read_csv`, `write_csv`, `read_json`, `write_json`
- `read_yaml`, `write_yaml`, `read_toml`, `write_toml`

#### Recursive Search
- `find_files_by_extension`, `find_files_by_pattern`
- `search_file_content`: Full-text search

#### Temp Management
- `create_temp_file`, `create_temp_directory`
- `temp_file_context`, `temp_dir_context`

### 🌐 HTTP Functions (`http_functions/`)
**9 functions** for HTTP operations:

- `http_get`, `http_post`, `http_put`, `http_delete`
- `download_file`: Streaming download with progress
- `upload_file`: Multipart file upload
- `parse_query_string`, `build_query_string`
- `get_response_headers`

### 🔄 Iterable Functions (`iterable_functions/`)
**55 functions** for advanced iteration and collection operations:

- **Chunking**: `chunk_list`, `sliding_window`, `batch_iterable`
- **Filtering**: `filter_none`, `filter_duplicates`, `filter_by_type`
- **Transformation**: `flatten`, `group_by`, `partition`
- **Aggregation**: `merge_dicts`, `deep_merge`, `reduce_by_key`
- **Utilities**: `first`, `last`, `nth`, `take`, `drop`

### 🧬 Bioinformatics Functions (`bioinformatics_functions/`)
**77 functions** for biological sequence analysis:

#### Sequence Operations
- Reverse complement, transcription, translation
- ORF finding, codon usage analysis

#### Alignment
- Needleman-Wunsch, Smith-Waterman algorithms
- Multiple sequence alignment

#### GC Content & Statistics
- GC content calculation, GC skew
- Sequence complexity analysis

#### Motif & Pattern Finding
- Motif discovery, consensus sequences
- Pattern matching with mismatches

#### Translation & Codon Usage
- Genetic code translation (standard + alternative codes)
- Codon frequency analysis

### 🧮 Mathematical Functions (`mathematical_functions/`)
**5 core functions** for numerical operations:

- `gcd`, `lcm`: Greatest common divisor and least common multiple
- `is_prime`: Primality testing
- `factorial`: Factorial computation
- `fibonacci`: Fibonacci sequence generation

### 🔐 Security Functions (`security_functions/`)
**12 functions** for cryptography and security:

- **Hashing**: `hash_password`, `verify_password` (bcrypt)
- **Encryption**: `encrypt_data`, `decrypt_data` (AES, RSA)
- **Tokens**: `generate_token`, `verify_token`
- **Keys**: `generate_key_pair`, `sign_data`, `verify_signature`

### 📊 Serialization Functions (`serialization_functions/`)
**28 functions** for advanced data serialization:

#### CSV Operations
- `stream_csv_chunks`: Memory-efficient streaming
- `merge_csv_files`: Merge multiple CSV files
- `transform_csv_columns`: Column transformations
- `validate_csv_structure`: Schema validation

#### Excel Operations
- `read_excel_sheet`, `write_excel_sheet`
- `merge_excel_sheets`: Multi-sheet merging
- `transpose_excel_data`, `auto_format_excel_columns`
- `read_excel_range`, `write_excel_range`

#### Parquet Operations
- `read_parquet`, `write_parquet`
- `merge_parquet_files`, `filter_parquet`
- `partition_parquet_by_column`: Efficient partitioning
- `get_parquet_schema`, `get_parquet_metadata`

#### Format Converters
- `csv_to_parquet`, `parquet_to_csv`
- `excel_to_parquet`, `parquet_to_excel`
- `excel_to_csv_batch`: Batch conversion

### 🔌 SSH Functions (`ssh_functions/`)
**12 functions** for SSH operations:

#### Remote Operations
- `execute_remote_command`: Remote command execution
- `upload_file`, `download_file`: SFTP transfers
- `list_remote_files`, `remote_file_exists`

#### Local Operations
- `execute_local_command`: Local command with SSH-like interface
- `create_ssh_key_pair`: Key generation

### 🧪 Testing Functions (`testing_functions/`)
**24 functions** for test utilities:

#### Fixtures & Mocks
- `create_temp_file_fixture`, `create_temp_dir_fixture`
- `mock_function`, `mock_class`
- `create_mock_response`: HTTP response mocking

#### Assertions
- `assert_equals_ignore_whitespace`
- `assert_json_equals`, `assert_xml_equals`
- `assert_raises_with_message`

#### Test Data Generators
- `generate_random_string`, `generate_random_number`
- `generate_test_dataframe`, `generate_test_json`

### 🌍 Network Functions (`network_functions/`)
**28 functions** for network operations:

- **IP Utilities**: `is_valid_ip`, `ip_in_range`, `get_ip_info`
- **DNS**: `resolve_hostname`, `reverse_dns_lookup`
- **Port Scanning**: `scan_port`, `scan_ports`
- **Connectivity**: `ping_host`, `check_port_open`

### 🌐 Web Scraping Functions (`web_scraping_functions/`)
**18 functions** for web scraping:

- **HTML Parsing**: `parse_html`, `extract_links`, `extract_text`
- **CSS Selectors**: `select_elements`, `get_attribute`
- **XPath**: `xpath_select`, `xpath_extract`
- **Advanced**: `scrape_table`, `extract_metadata`

### 🔗 URL Functions (`url_functions/`)
**8 functions** for URL manipulation:

- `parse_url`, `build_url`, `normalize_url`
- `validate_url_format`, `extract_domain`
- `add_query_params`, `remove_query_params`

### 🖨️ Print Functions (`print_functions/`)
**3 utilities** for enhanced console output:

- `print_colored`: ANSI color support
- `print_table`: Tabular data formatting
- `print_progress_bar`: Progress visualization

### 🔍 Regex Functions (`regex_functions/`)
**5 functions** for regular expressions:

- `validate_email`, `validate_phone`, `validate_url`
- `extract_emails`, `extract_urls`

### ⚙️ CLI Functions (`cli_functions/`)
**16 functions** for system operations:

- **System Info**: `get_cpu_info`, `get_memory_info`, `get_disk_usage`
- **Process Management**: `is_process_running`, `kill_process`
- **File System**: `list_files`, `list_directories`, `get_file_size`
- **Environment**: `get_environment_variable`, `set_environment_variable`

### 📝 Logger Functions (`logger_functions/`)
**7 functions** for logging utilities:

- `setup_logger`: Configurable logger creation
- `log_function_call`: Automatic function logging
- `log_exception`: Exception logging with context
- `create_rotating_logger`: Rotating file handler

### 🔄 Multiprocessing Functions (`multiprocessing_functions/`)
**19 functions** for parallel processing:

- **Pool Management**: `create_pool`, `parallel_map`, `parallel_starmap`
- **Process Control**: `run_in_process`, `terminate_pool`
- **Utilities**: `get_cpu_count`, `split_work`

### 🔧 Batch Processing Functions (`batch_processing_functions/`)
**2 classes** for efficient data processing:

- `ChunkedProcessor`: Memory-efficient batch processing
- `StreamingAggregator`: Real-time data aggregation

### 🌿 Environment Config Functions (`env_config_functions/`)
**6 functions** for configuration management:

- `load_env_file`, `get_env_variable`, `set_env_variable`
- `load_yaml_config`, `load_toml_config`
- `merge_configs`: Hierarchical configuration merging

### ✅ Data Validation (`data_validation/`)
**Multiple submodules** for data validation:

#### Basic Validation
- Type checking, range validation, format validation
- String validation (email, phone, URL, etc.)

#### Schema Validation
- JSON Schema validation
- Custom schema definition and validation
- Nested structure validation

### 🛠️ Development Utilities (`dev_utilities/`)
Utilities for development workflows:

- Code generation helpers
- AST manipulation utilities
- Development environment tools

## 🔑 Key Features

### Database-Agnostic Design
All database functions use **SQLAlchemy** for maximum portability:
- ✅ PostgreSQL
- ✅ MySQL / MariaDB
- ✅ SQLite
- ✅ Oracle
- ✅ SQL Server

### Type Safety
- Complete type hints using modern Python syntax (`list[str]`, `dict[str, Any]`)
- Runtime type checking with decorators
- mypy-compliant codebase

### Comprehensive Testing
- 88%+ test coverage
- 150+ test files with 1000+ test cases
- Pytest-based testing framework
- Comprehensive edge case coverage

### Documentation
- NumPy-style docstrings for all functions
- Examples in docstrings
- Time/space complexity notes for algorithms
- Comprehensive README with usage examples

## 📚 Usage Examples

### Database Operations
```python
from database_functions import create_connection, atomic_transaction, execute_query
from database_functions.schema_inspection import (
    get_table_info,
    find_duplicate_rows,
    get_foreign_key_dependencies
)

# Create connection
conn = create_connection("postgresql://user:pass@localhost/db")

# Safe transaction
with atomic_transaction(conn) as trans:
    execute_query(trans, "INSERT INTO users VALUES (:name)", {"name": "John"})

# Schema inspection
table_info = get_table_info(conn, "users")
print(f"Columns: {table_info['columns']}")

# Find duplicates
duplicates = find_duplicate_rows(conn, "users", ["email"])

# Get FK dependencies for safe operations
deps = get_foreign_key_dependencies(conn)
print(f"Safe drop order: {deps['ordered_tables']}")
```

### Async Operations
```python
from asyncio_functions import async_batch, fetch_multiple_urls, AsyncConnectionPool

# Batch processing
async def process_items():
    results = await async_batch(
        items=range(100),
        func=process_item,
        batch_size=10
    )
    return results

# HTTP fetching
urls = ["https://api.example.com/1", "https://api.example.com/2"]
responses = await fetch_multiple_urls(urls, max_concurrent=5)

# Connection pooling
async with AsyncConnectionPool("postgresql://...") as pool:
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM users")
```

### Decorators
```python
from decorators import cache, retry, timeout, enforce_types

@cache(maxsize=128, ttl=3600)
@retry(max_attempts=3, backoff=2.0)
@timeout(seconds=30)
@enforce_types
def fetch_user_data(user_id: int) -> dict:
    # Function logic here
    return {"id": user_id, "name": "John"}
```

### File Operations
```python
from file_functions import read_file_lines, hash_file, find_files_by_pattern
from file_functions import temp_file_context

# Read file
lines = read_file_lines("data.txt", encoding="utf-8")

# Hash file
file_hash = hash_file("document.pdf", algorithm="sha256")

# Find files
python_files = find_files_by_pattern("/project", "*.py")

# Temp file context
with temp_file_context(suffix=".txt") as temp_path:
    # Use temp file
    temp_path.write_text("temporary data")
```

### Data Serialization
```python
from serialization_functions import (
    stream_csv_chunks,
    csv_to_parquet,
    read_excel_sheet
)

# Stream large CSV
for chunk in stream_csv_chunks("large_file.csv", chunk_size=10000):
    process_chunk(chunk)

# Convert formats
csv_to_parquet("input.csv", "output.parquet", compression="snappy")

# Read Excel
data = read_excel_sheet("report.xlsx", sheet_name="Sales")
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific module tests
python -m pytest pytest/unit/database_functions/
```

## 📋 Requirements

- **Python**: 3.10 or higher
- **Core Dependencies**: Listed in `pyproject.toml`
- **Optional Dependencies**: 
  - `pyarrow` for Parquet operations
  - `openpyxl` for Excel operations
  - `paramiko` for SSH operations
  - `bcrypt` for password hashing

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow the existing code style and patterns
2. Add comprehensive docstrings (NumPy style)
3. Include type hints for all functions
4. Write unit tests with 95%+ coverage
5. Update documentation as needed

See `.github/copilot-instructions.md` for detailed development guidelines.

## 📝 Version Management

This package uses centralized version management:
- **Single source**: Version defined in `_version.py`
- **Automatic**: All modules import from `_version.py`
- **Dynamic**: `pyproject.toml` reads version at build time
- **Update**: Change version in one place: `_version.py`

## 📄 License

MIT License - see LICENSE file for details.

## 👤 Author

**MForofontov**
- GitHub: [@MForofontov](https://github.com/MForofontov)

## 🔗 Links

- **Repository**: https://github.com/MForofontov/python-utils
- **Issues**: https://github.com/MForofontov/python-utils/issues
- **Documentation**: https://github.com/MForofontov/python-utils#readme

---

⭐ **Star this repository** if you find it useful!
