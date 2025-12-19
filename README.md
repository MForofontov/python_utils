# Python Utilities

A comprehensive collection of reusable Python utilities and functions covering a wide range of programming tasks. This library provides modular, well-tested, and documented functions organized by domain to help accelerate development across various Python projects.

## 🚀 Overview

This repository contains over 200+ utility functions, classes, and decorators organized into 14 specialized modules. Each module focuses on a specific domain and provides production-ready implementations with comprehensive documentation, type hints, and unit tests.

## 📦 Installation

### From Source
```bash
git clone https://github.com/MForofontov/python-utils.git
cd python-utils
pip install .
```

### Development Installation
```bash
git clone https://github.com/MForofontov/python-utils.git
cd python-utils
pip install -e ".[dev]"
```

## 🗂️ Module Structure

### 🔄 Asyncio Functions (`asyncio_functions/`)
Advanced asynchronous programming utilities for building robust async applications:

- **Task Management**: `async_batch`, `async_chain`, `async_throttle`, `async_timeout`
- **Error Handling**: `async_await_with_error_handling`, `async_retry_with_backoff`
- **Resource Management**: `AsyncConnectionPool`, `use_connection`, `async_cleanup`
- **Rate Limiting**: `async_rate_limited`, `async_periodic`
- **Concurrency**: `gather_with_timeout`, `run_in_parallel`, `async_map`
- **HTTP Utilities**: `fetch`, `fetch_all`
- **Stream Processing**: `async_stream_processor`
- **Task Control**: `async_cancellable_task`

**Key Features:**
- Connection pooling for database/HTTP connections
- Configurable retry mechanisms with exponential backoff
- Rate limiting and throttling for API calls
- Stream processing for large datasets
- Graceful cleanup and cancellation handling

### 🗜️ Compression Functions (`compression_functions/`)
Comprehensive data compression utilities supporting multiple algorithms:

#### Binary Compression
- **Algorithms**: GZIP, BZ2, LZMA, Zlib, Snappy, Zstandard
- **Functions**: `compress_data`, `decompress_data` with auto-detection
- **Performance**: Optimized for speed and compression ratio

#### File Compression
- **Archive Formats**: ZIP, TAR (with GZIP/BZ2/LZMA)
- **File Operations**: `compress_zip`, `decompress_file_zip`, `compress_tar`
- **Batch Processing**: Handle multiple files and directories

#### Specialized Compression
- **Polyline Encoding**: `polyline_encoding_list_of_ints`, `polyline_decoding_list_of_ints`
- **Number Compression**: `decompress_number` for numerical data

### 🎨 Decorators (`decorators/`)
Powerful decorators for function enhancement and cross-cutting concerns:

#### Performance & Monitoring
- `@time_function`: Execution time measurement
- `@time_and_resource_function`: CPU, memory, and time profiling
- `@cache`: Function result caching with TTL
- `@cache_with_expiration`: Time-based cache invalidation

#### Error Handling & Resilience
- `@handle_error`: Comprehensive error handling with logging
- `@async_handle_error`: Async-specific error management
- `@retry`: Configurable retry logic with backoff
- `@timeout`: Function execution timeouts

#### Input/Output Processing
- `@enforce_types`: Runtime type checking
- `@validate_args`: Argument validation
- `@normalize_input`: Input data normalization
- `@format_output`: Output formatting and serialization
- `@serialize_output`: JSON/pickle serialization

#### Control Flow
- `@conditional_execute`: Conditional function execution
- `@conditional_return`: Smart return value handling
- `@rate_limit`: Function call rate limiting
- `@throttle`: Request throttling
- `@deprecated`: Deprecation warnings

#### Development & Debugging
- `@log_function_calls`: Comprehensive call logging
- `@log_signature`: Function signature logging
- `@redirect_output`: Output redirection
- `@multi_decorator`: Decorator composition
- `@chain`: Function chaining

#### Advanced Features
- `@async_wrapper`: Sync-to-async conversion
- `@event_trigger`: Event-driven programming
- `@env_config`: Environment-based configuration
- `@requires_permission`: Permission-based access control

### 🏗️ Data Types (`data_types/`)
Complete implementations of fundamental data structures:

#### Trees
- **AVL Tree**: `AVLNode`, `AVLTree` - Self-balancing binary search tree
- **Red-Black Tree**: `RedBlackNode`, `RedBlackTree` - Balanced binary tree
- **Splay Tree**: `SplayNode`, `SplayTree` - Self-adjusting binary tree
- **Binary Tree**: `BinaryTreeNode`, `BinaryTree` - Basic binary tree
- **Segment Tree**: `SegmentTree` - Range query optimization
- **Trie**: `TrieNode`, `Trie` - Prefix tree for string operations

#### Linear Data Structures
- **Linked List**: `Node`, `LinkedList` - Dynamic linear structure
- **Stack**: `Stack` - LIFO data structure
- **Queue**: `Queue` - FIFO data structure
- **Deque**: `Deque` - Double-ended queue
- **Circular Queue**: `CircularQueue` - Fixed-size circular buffer

#### Advanced Structures
- **Graph**: `Graph` - Adjacency list representation with algorithms
- **Hash Table**: `HashTable` - Custom hash table implementation
- **Binary Heap**: `BinaryHeap` - Min/max heap operations
- **Priority Queue**: `PriorityQueue` - Priority-based queue
- **Skip List**: `SkipNode`, `SkipList` - Probabilistic data structure
- **Union Find**: `UnionFind` - Disjoint set data structure

### 📅 Datetime Functions (`datetime_functions/`)
Comprehensive date and time manipulation utilities:

#### Date Operations
- **Calculations**: `calculate_age`, `days_between`, `time_ago`, `time_until`
- **Comparisons**: `compare_dates`, `is_today`, `is_weekend`, `is_leap_year`
- **Parsing**: `parse_date`, `format_date`, `get_current_datetime_iso`

#### Date Components
- **Extraction**: `get_date_parts`, `get_week_number`, `get_days_in_month`
- **Calendar**: `get_days_of_week`, `get_start_of_week`, `get_end_of_week`

#### Date Manipulation
- **Modification**: `modify_days`, `modify_weeks`, `modify_months`, `modify_years`
- **Boundaries**: `get_start_of_month`, `get_end_of_month`, `get_start_of_year`, `get_end_of_year`
- **Timezone**: `convert_timezone`

### 📁 File Functions (`file_functions/`)
Robust file system operations and data processing:

#### File Operations
- **Basic**: `copy_file`, `check_and_delete_file`, `write_to_file`
- **Directory**: `create_directory`, `copy_folder`, `merge_folders`, `cleanup`
- **Path Utilities**: `join_paths`, `file_basename`, `get_paths_dict`

#### File Discovery
- **Search**: `get_paths_in_directory`, `get_paths_in_directory_with_suffix`
- **Filtering**: Support for pattern matching and recursive search

#### Data Processing
- **Text Files**: `read_lines`, `write_lines`, `concat_files`
- **Tabular Data**: `read_tabular` - CSV/TSV parsing with custom delimiters
- **JSON**: `json_to_dict`, `write_dict_to_json` - JSON file operations
- **TSV**: `tsv_to_dict`, `write_dict_to_tsv` - Tab-separated value handling

### 🌐 HTTP Functions (`http_functions/`)
HTTP client utilities for web API interactions:

- **Request Methods**: Support for GET, POST, PUT, DELETE, PATCH
- **Authentication**: Basic, Bearer token, API key support
- **Session Management**: Persistent connections and cookie handling
- **Error Handling**: Retry logic and timeout management
- **Response Processing**: JSON parsing and error detection

### 🔧 Iterable Functions (`iterable_functions/`)
Advanced operations for Python iterables and data structures:

#### List Operations
- **Manipulation**: `flatten_list`, `divide_list_into_n_chunks`
- **Search**: `find_sublist_index`, `get_max_min_values`
- **Analysis**: `identify_dict_structure`

#### Data Processing
- **Transformation**: Element-wise operations and filtering
- **Aggregation**: Statistical operations on iterables
- **Validation**: Structure and type checking

### 📊 JSON Functions (`json_functions/`)
JSON data manipulation and validation utilities:

- **Parsing**: Safe JSON parsing with error handling
- **Validation**: Schema validation and structure checking
- **Transformation**: JSON-to-object and object-to-JSON conversion
- **Merging**: Deep merge operations for complex JSON structures

### 💻 CLI Functions (`cli_functions/`)
Cross-platform command-line interface and system utilities:

#### Command Execution
- **execute_command**: Execute shell commands with timeout and error handling
- **check_command_exists**: Verify command availability in system PATH

#### Environment Management
- **get_environment_variable**: Retrieve environment variables with validation
- **set_environment_variable**: Set environment variables safely

#### System Information
- **get_cpu_info**: CPU statistics and usage monitoring
- **get_memory_info**: Memory usage and statistics
- **get_disk_usage**: Disk space and usage information
- **get_network_info**: Network interface details
- **get_uptime**: System uptime tracking
- **get_current_user**: Current system user information
- **get_hostname**: System hostname retrieval

#### Process Management
- **is_process_running**: Check if process is running by name
- **kill_process**: Terminate process by PID

#### File Operations
- **get_file_size**: Get file size in bytes
- **list_files**: List files in directory
- **list_directories**: List subdirectories

### 🔧 Logger Functions (`logger_functions/`)
Advanced logging configuration and management:

- **Logger Creation**: `get_logger` - Configured logger instances
- **Validation**: `validate_logger` - Logger configuration verification
- **Formatting**: Custom formatters for different output formats
- **Handlers**: File, console, and rotating log handlers

### ⚡ Multiprocessing Functions (`multiprocessing_functions/`)
Parallel processing utilities for CPU-intensive tasks:

- **Process Pools**: Managed worker processes
- **Task Distribution**: Automatic workload balancing
- **Result Aggregation**: Efficient result collection
- **Error Handling**: Process failure recovery

### 🖨️ Print Functions (`print_functions/`)
Enhanced console output and system information display:

- **Formatted Output**: `print_message` - Styled console messages
- **System Info**: `print_system_info_in_terminal` - Hardware and OS details
- **Dependencies**: `print_dependencies_info_in_terminal` - Package information
- **Styling**: Color support and formatting options

### 📈 Statistics Functions (`statistics_functions/`)
Mathematical and statistical computation utilities:

- **Descriptive Statistics**: Mean, median, mode, standard deviation
- **Distributions**: Normal, binomial, and custom distributions
- **Correlation**: Pearson and Spearman correlation coefficients
- **Regression**: Linear and polynomial regression analysis

### 🔤 String Utilities (`strings_utility/`)
Comprehensive string manipulation and processing:

- **Formatting**: Case conversion, padding, and alignment
- **Validation**: Pattern matching and format verification
- **Transformation**: Encoding, escaping, and normalization
- **Parsing**: String tokenization and extraction

## 🛠️ Dependencies

### Core Dependencies
- **cramjam** (2.11.0) - Fast compression/decompression
- **python-snappy** (0.7.3) - Snappy compression bindings
- **zstandard** (0.23.0) - Zstandard compression
- **psutil** (7.0.0) - System and process utilities
- **tqdm** (4.67.1) - Progress bars
- **numpy** (2.3.2) - Numerical computing
- **aiohttp** (3.12.15) - Async HTTP client/server
- **pandas** (2.3.1) - Data manipulation and analysis

### Development Dependencies
- **pytest** (8.4.1) - Testing framework
- **pytest-asyncio** (1.1.0) - Async testing support
- **allure-pytest** (2.15.0) - Test reporting
- **pylint** (3.3.7) - Code analysis
- **mypy** (1.17.1) - Static type checking

## 🧪 Testing

The project includes comprehensive unit tests for all modules:

```bash
# Run all tests
pytest

# Run tests for specific module
pytest pytest/unit/asyncio_functions/

# Run with coverage
pytest --cov=. --cov-report=html

# Run with allure reporting
pytest --alluredir=allure-results
allure serve allure-results
```

All tests that involve randomness use a fixed seed (`random.seed(0)`) to ensure reproducible results.

### Test Structure
```
pytest/
├── conftest.py              # Test configuration
└── unit/                    # Unit tests
    ├── asyncio_functions/   # Async function tests
    ├── compression_functions/ # Compression tests
    ├── data_types/          # Data structure tests
    ├── decorators/          # Decorator tests
    └── ...                  # Other module tests
```

## 📚 Usage Examples

### Asyncio Functions
```python
from asyncio_functions import async_retry_with_backoff, fetch_all, AsyncConnectionPool

# Retry with exponential backoff
@async_retry_with_backoff(max_retries=3, base_delay=1.0)
async def unreliable_api_call():
    # Your async function here
    pass

# Fetch multiple URLs concurrently
urls = ['http://api1.com', 'http://api2.com']
results = await fetch_all(urls, max_concurrent=10)

# Connection pooling
async with AsyncConnectionPool(max_connections=5) as pool:
    async with use_connection(pool) as conn:
        # Use connection
        pass
```

### Decorators
```python
from decorators import cache, time_function, handle_error, validate_args

# Function caching
@cache(maxsize=100, ttl=300)
def expensive_computation(x, y):
    return x ** y

# Performance monitoring
@time_function
def slow_function():
    # Function implementation
    pass

# Error handling
@handle_error(default_return=None, log_errors=True)
def risky_function():
    # Function that might fail
    pass

# Argument validation
@validate_args(types={'x': int, 'y': str})
def typed_function(x: int, y: str):
    return f"{y}: {x}"
```

### Data Types
```python
from data_types import AVLTree, Graph, HashTable, Trie

# Self-balancing tree
tree = AVLTree()
tree.insert(10)
tree.insert(5)
tree.insert(15)

# Graph operations
graph = Graph()
graph.add_edge('A', 'B', weight=5)
path = graph.shortest_path('A', 'B')

# Hash table
ht = HashTable(capacity=100)
ht.put('key', 'value')

# Trie for string operations
trie = Trie()
trie.insert('hello')
trie.insert('world')
suggestions = trie.get_words_with_prefix('hel')
```

### File Operations
```python
from file_functions import read_tabular, write_dict_to_json, copy_folder

# Read CSV/TSV files
data = read_tabular('data.csv', delimiter=',', headers=True)

# JSON operations
data = {'name': 'John', 'age': 30}
write_dict_to_json(data, 'output.json')

# Directory operations
copy_folder('source/', 'destination/', overwrite=True)
```

### Compression
```python
from compression_functions import compress_data, decompress_data, compress_zip

# Automatic compression
data = b"Hello, World!" * 1000
compressed = compress_data(data, algorithm='gzip')
decompressed = decompress_data(compressed)

# File compression
compress_zip(['file1.txt', 'file2.txt'], 'archive.zip')
```

## 🔧 Configuration

### Environment Variables
Many functions support configuration through environment variables:

```bash
# Logging configuration
export LOG_LEVEL=DEBUG
export LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# HTTP client settings
export HTTP_TIMEOUT=30
export HTTP_MAX_RETRIES=3

# Compression settings
export DEFAULT_COMPRESSION='gzip'
export COMPRESSION_LEVEL=6
```

### Configuration Files
Some modules support configuration files (JSON/YAML):

```json
{
  "async_settings": {
    "max_concurrent_requests": 10,
    "timeout": 30,
    "retry_attempts": 3
  },
  "compression": {
    "default_algorithm": "gzip",
    "compression_level": 6
  }
}
```

## 🏗️ Architecture

### Design Principles
1. **Modularity**: Each module is self-contained and independently usable
2. **Type Safety**: Comprehensive type hints throughout the codebase
3. **Error Handling**: Robust error handling with informative messages
4. **Performance**: Optimized implementations for common use cases
5. **Documentation**: Extensive docstrings with examples
6. **Testing**: High test coverage with unit and integration tests

### Code Quality
- **Static Analysis**: pylint and mypy for code quality
- **Formatting**: Consistent code style
- **Documentation**: NumPy-style docstrings
- **Version Control**: Semantic versioning

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone https://github.com/MForofontov/python-utils.git
cd python-utils

# Install in development mode
pip install -e ".[dev]"

# Run quality checks
pylint python_utils/
mypy python_utils/
pytest
```

### Contribution Guidelines
1. **Code Style**: Follow PEP 8 and existing patterns
2. **Documentation**: Add docstrings for all public functions
3. **Testing**: Include unit tests for new functionality
4. **Type Hints**: Add type annotations for all parameters and returns
5. **Error Handling**: Include appropriate error handling and validation

### Adding New Modules
1. Create module directory with `__init__.py`
2. Implement functions with proper documentation
3. Add comprehensive unit tests
4. Update main `__init__.py` and documentation
5. Run full test suite

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/MForofontov/python-utils
- **Documentation**: [Coming Soon]
- **Issues**: https://github.com/MForofontov/python-utils/issues
- **Discussions**: https://github.com/MForofontov/python-utils/discussions

## 📝 Changelog

### Version 0.1.0
- Initial release with 14 core modules
- Over 200+ utility functions and classes
- Comprehensive test suite
- Full type annotation support
- Documentation and examples

---

**Made with ❤️ by the Python Utils Team**

## Running Tests

You **must** install the development dependencies before running tests. Use
`pip install -r requirements_dev.txt` or install the optional `dev` extras via
`pip install -e .[dev]`. These packages include `pytest` and
`pytest-asyncio` in addition to the runtime requirements. If they are missing,
tests will raise import errors. After installing the dependencies, you can run
all tests and generate an Allure report using the helper script:

```bash
bash pytest.sh
```

The script runs tests from `pytest/unit` and stores the report under `pytest_run_tests/`.
The Allure command-line tool is required to generate the reports. If you don't have it installed, follow the [official installation guide](https://docs.qameta.io/allure/#_installing_a_commandline).

## Example Usage

Import modules directly from the package. For example, to capitalize each word in a string:

```python
from strings_utility.capitalize_words import capitalize_words

print(capitalize_words("hello world"))  # -> 'Hello World'
```

## Logging

Set up a logger once in your application and pass it to any decorator that
accepts the optional ``logger`` parameter.

```python
import logging

logger = logging.getLogger("python_utils")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

from decorators.throttle import throttle

@throttle(0.5, logger=logger)
def my_function():
    ...
```

The `timeout` decorator is also thread-based so it works on all platforms,
including Windows. When the specified limit is reached a `TimeoutException` is
raised while the underlying thread may still finish in the background.

## Contributing

1. Fork the repository and create a new branch.
2. Make your changes and add tests when appropriate.
3. Commit your work and open a pull request.

## Authors

- [Mykyta Forofontov](https://github.com/MForofontov)

## License

This project is licensed under the [GNU GPLv3](LICENSE).

