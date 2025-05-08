# Python Functions Repository

This repository contains various Python functions and utilities organized into different folders. Each folder contains specific functionalities and their corresponding unit tests.

## Folder Structure

The repository is organized into several folders, each containing specific functionalities:

- **asyncio-functions**: Contains functions and utilities for asynchronous programming using `asyncio`.
- **compression_functions**: Includes functions for compressing and decompressing data using various algorithms such as BZ2, GZIP, LZMA, Snappy, Zlib, and Zstandard.
- **file-functions**: Provides utilities for file operations such as creating directories, reading and writing tabular data, and handling file I/O.
- **iterable_functions**: Contains functions for manipulating and processing iterables, such as lists and sets.
- **linux-functions**: Includes utilities for monitoring and managing Linux system resources and processes.
- **multiprocessing-functions**: Provides functions for parallel processing using Python's `multiprocessing` module.
- **pandas-functions**: Contains utilities for working with `pandas` DataFrames, including filtering, merging, reading, and writing data.
- **statistics-functions**: Includes functions for statistical calculations such as mean, median, mode, standard deviation, and variance.
- **strings_utility**: Provides various string manipulation functions, including capitalization, centering, joining, splitting, and more.
- **wrappers**: Contains decorator functions for enhancing and modifying the behavior of other functions.

## Requirements

The repository uses the following Python packages, as specified in `requirements.txt`:
- allure-pytest==2.13.5
- allure-python-commons==2.13.5
- attrs==24.2.0
- cramjam==2.9.0
- exceptiongroup==1.2.2
- iniconfig==2.0.0
- packaging==24.2
- pluggy==1.5.0
- pytest==8.3.3
- python-snappy==0.7.3
- tomli==2.1.0
- zstandard==0.23.0

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/MForofontov/Python-functions
    cd Python-functions
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running Tests

To run the unit tests, use the following command:
```sh
pytest --alluredir "path/to/allure/output" --cov="path/to/code/to/calculate/cov" --cov-report=xml:"path/to/xml/output
```

To run the unit tests and generate the report, use the following command:
```sh
pytest.sh
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.
