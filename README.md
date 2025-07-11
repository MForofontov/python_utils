# Python Utilities

A collection of reusable Python functions covering a wide range of tasks. The project is organized into folders by topic and includes unit tests for each module.

## Contents

- **asyncio_functions/** – helpers for asynchronous programming such as task throttling, retries and timeouts.
- **compression_functions/** – utilities for compressing and decompressing data with algorithms like BZ2, GZIP, LZMA, Snappy, Zlib and Zstandard.
- **decorators/** – decorator functions for caching, conditional execution and error handling.
- **file_functions/** – file system helpers for copying files, creating directories and parsing tabular data.
- **iterable_functions/** – operations for lists, sets and other iterables.
- **linux_functions/** – utilities for monitoring Linux processes and resources.
- **multiprocessing_functions/** – patterns for parallel processing using the `multiprocessing` module.
- **pandas_functions/** – simple wrappers around common `pandas` DataFrame tasks.
- **print_functions/** – print formatted messages and system information to the terminal.
- **statistics_functions/** – basic statistical calculations.
- **strings_utility/** – handy string manipulation helpers.
- **data_types/** – implementations of data structures such as graphs, heaps and queues.

## Installation

```bash
# clone the repository
git clone https://github.com/MForofontov/python-utils
cd python-utils

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# install dependencies
pip install -r requirements.txt
```

## Running Tests

The repository uses `pytest`. You can run all tests and generate an Allure report using the helper script:

```bash
bash pytest.sh
```

The script runs tests from `pytest/unit` and stores the report under `pytest_run_tests/`.

## Example Usage

Import modules directly from the package. For example, to capitalize each word in a string:

```python
from strings_utility.capitalize_words import capitalize_words

print(capitalize_words("hello world"))  # -> 'Hello World'
```

## Contributing

1. Fork the repository and create a new branch.
2. Make your changes and add tests when appropriate.
3. Commit your work and open a pull request.

## License

This project is licensed under the [GNU GPLv3](LICENSE).
