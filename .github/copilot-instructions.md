# GitHub Copilot Instructions for Python Utilities Repository

## Repository Overview

This is a comprehensive Python utilities library containing 200+ reusable functions, classes, and decorators organized into 14 specialized modules. The codebase follows strict patterns for maintainability, type safety, and testing coverage.

## Project Structure and Logic

### 1. Modular Organization
The repository is organized into domain-specific modules:
- `asyncio_functions/` - Asynchronous programming utilities
- `compression_functions/` - Data compression algorithms
- `data_types/` - Data structure implementations
- `datetime_functions/` - Date and time utilities
- `decorators/` - Function enhancement decorators
- `env_config_functions/` - Environment configuration
- `file_functions/` - File system operations
- `http_functions/` - HTTP client utilities
- `iterable_functions/` - Iterator and list operations
- `json_functions/` - JSON manipulation
- `linux_functions/` - System monitoring
- `logger_functions/` - Logging utilities
- `multiprocessing_functions/` - Parallel processing
- `print_functions/` - Enhanced console output
- `strings_utility/` - String manipulation

Each module contains:
- Individual function files with descriptive names
- `__init__.py` with proper exports using `__all__`
- Comprehensive unit tests in `pytest/unit/`

### 2. Core Design Principles

#### Type Safety
- **ALL functions must have complete type hints**
- Use `typing` and `collections.abc` imports appropriately
- Define generic type variables when needed (`T`, `R`, etc.)
- Include both parameter and return type annotations

#### Error Handling
- Validate input parameters with descriptive error messages
- Use specific exception types (TypeError, ValueError, etc.)
- Include parameter name in error messages for clarity
- Handle edge cases gracefully

#### Documentation
- Use NumPy-style docstrings for all public functions
- Include Parameters, Returns, and Examples sections
- Provide working code examples in docstrings
- Document exceptions that may be raised

## Coding Standards and Best Practices

### 1. Function Structure Template

```python
from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")
R = TypeVar("R")

def function_name(
    param1: int,
    param2: str,
    optional_param: bool = False,
) -> ReturnType:
    """
    Brief description of what the function does.

    Parameters
    ----------
    param1 : int
        Description of param1.
    param2 : str
        Description of param2.
    optional_param : bool, optional
        Description of optional parameter (by default False).

    Returns
    -------
    ReturnType
        Description of return value.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> function_name(42, "hello")
    ExpectedOutput
    """
    # Input validation
    if not isinstance(param1, int):
        raise TypeError("param1 must be an integer")
    if not isinstance(param2, str):
        raise TypeError("param2 must be a string")
    
    # Function logic here
    result = # computation
    
    return result


__all__ = ['function_name']
```

### 2. Module __init__.py Structure

```python
from .function1 import function1
from .function2 import function2
from .subfolder.function3 import function3

__all__ = [
    'function1',
    'function2', 
    'function3',
]
```

### 3. Test Structure Template

```python
import pytest
from module_name.function_name import function_name


def test_function_name_basic() -> None:
    """
    Test case 1: Basic functionality description.
    """
    # Test data
    input_data = # test input
    expected = # expected output
    
    # Execute
    result = function_name(input_data)
    
    # Assert
    assert result == expected


def test_function_name_edge_case() -> None:
    """
    Test case 2: Edge case description.
    """
    # Test edge case behavior
    result = function_name(edge_case_input)
    assert result == expected_edge_result


def test_function_name_error_handling() -> None:
    """
    Test case 3: Error handling validation.
    """
    with pytest.raises(TypeError, match="specific error message"):
        function_name(invalid_input)


def test_function_name_type_validation() -> None:
    """
    Test case 4: Type validation.
    """
    with pytest.raises(TypeError):
        function_name("wrong_type")
```

### 4. Decorator Implementation Patterns

When creating decorators, follow this pattern:

```python
import logging
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def decorator_name(
    param: str,
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator description.
    
    Parameters
    ----------
    param : str
        Description of parameter.
    logger : logging.Logger | None, optional
        Logger instance (by default None).
    """
    # Input validation
    if not isinstance(param, str):
        raise TypeError("param must be a string")
    if logger is not None and not isinstance(logger, logging.Logger):
        raise TypeError("logger must be an instance of logging.Logger or None")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                # Pre-processing logic
                result = func(*args, **kwargs)
                # Post-processing logic
                return result
            except Exception as e:
                if logger:
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator
```

### 5. Async Function Patterns

For async utilities:

```python
import asyncio
from typing import TypeVar, Any

T = TypeVar("T")

async def async_function_name(
    param: Any,
    timeout: float = 30.0,
) -> T:
    """
    Async function description.
    """
    try:
        async with asyncio.timeout(timeout):
            # Async logic here
            result = await some_async_operation(param)
            return result
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout} seconds")
```

## Testing Requirements

### 1. Test Coverage
- **Every function must have comprehensive unit tests**
- Test normal operation, edge cases, and error conditions
- Use descriptive test names with case numbers
- Include docstrings for all test functions

### 2. Test Organization
- Mirror the source code structure in `pytest/unit/`
- One test file per source module
- Use `pytest.raises()` for exception testing with specific error messages
- Use fixtures for complex setup when needed

### 3. Test Data
- Use `random.seed(0)` for reproducible random tests  
- Include both simple and complex test cases
- Test boundary conditions and invalid inputs

## Dependencies and Imports

### Core Dependencies
The project uses these main dependencies:
- `numpy` - Numerical computing
- `aiohttp` - Async HTTP operations  
- `psutil` - System utilities
- `tqdm` - Progress bars
- `cramjam`, `python-snappy`, `zstandard` - Compression

### Import Guidelines
- Use specific imports rather than wildcards
- Import from `collections.abc` for abstract base classes
- Use `typing` for type hints
- Import third-party libraries only when needed in the specific function

## Performance Considerations

### 1. Memory Efficiency
- Use generators for large datasets when possible
- Implement chunking for batch processing
- Clean up resources properly (use context managers)

### 2. CPU Optimization
- Leverage multiprocessing for CPU-intensive tasks
- Use appropriate chunk sizes for parallel processing
- Consider async patterns for I/O-bound operations

### 3. Caching
- Implement caching decorators where beneficial
- Use TTL (time-to-live) for cache expiration
- Consider memory usage in cache implementations

## Common Implementation Patterns

### 1. Input Validation Pattern
```python
def validate_inputs(param1: Any, param2: Any) -> None:
    """Validate function inputs with descriptive errors."""
    if not isinstance(param1, expected_type):
        raise TypeError(f"param1 must be {expected_type.__name__}, got {type(param1).__name__}")
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
```

### 2. Resource Management Pattern
```python
def function_with_resources(file_path: str) -> Any:
    """Properly manage resources using context managers."""
    try:
        with open(file_path, 'r') as file:
            # Process file
            return result
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error processing file {file_path}: {e}")
```

### 3. Configuration Pattern
```python
def configurable_function(
    data: Any,
    config: dict[str, Any] | None = None,
) -> Any:
    """Support configuration through optional parameters."""
    default_config = {
        'timeout': 30,
        'retries': 3,
        'batch_size': 100,
    }
    
    if config:
        default_config.update(config)
    
    # Use merged configuration
    return process_with_config(data, default_config)
```

## Specific Module Guidelines

### Decorators
- Always use `functools.wraps` to preserve metadata
- Support optional logger parameter for debugging
- Validate decorator parameters before function execution
- Handle both sync and async functions when applicable

### Data Types
- Implement standard methods (`__str__`, `__repr__`, etc.)
- Include proper type hints for generic classes
- Implement comparison operators when logical
- Provide clear examples of usage

### File Functions  
- Use pathlib for path operations when possible
- Handle file permissions and access errors
- Support both relative and absolute paths
- Implement proper cleanup for temporary files

### HTTP Functions
- Include timeout handling
- Support various authentication methods
- Handle HTTP errors gracefully
- Provide retry mechanisms for reliability

## Quality Assurance

### 1. Static Analysis
- Code must pass `pylint` checks
- Use `mypy` for type checking
- Follow PEP 8 style guidelines
- Maintain consistent formatting

### 2. Documentation
- All public functions require docstrings
- Include practical examples in docstrings
- Update README.md when adding new modules
- Document any breaking changes

### 3. Version Control
- Use semantic versioning
- Write descriptive commit messages
- Include tests with new features
- Update __all__ exports appropriately

## AI Assistant Guidelines

When working with this codebase:

1. **Always follow the established patterns** - Don't introduce new styles
2. **Include comprehensive type hints** - This is non-negotiable
3. **Write tests first** - Test-driven development is preferred
4. **Validate inputs thoroughly** - Better to be explicit about requirements
5. **Document everything** - Future maintainers will thank you
6. **Consider performance** - Especially for utilities that might process large datasets
7. **Handle errors gracefully** - Provide actionable error messages
8. **Use existing utilities** - Don't reinvent the wheel if functionality already exists
9. **Follow the module structure** - Keep related functionality together
10. **Update __all__ lists** - Ensure proper module exports

Remember: This is a utility library that other developers will depend on. Code quality, reliability, and clarity are paramount.
