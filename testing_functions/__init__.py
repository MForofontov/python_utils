"""
Testing functions module: Comprehensive testing utilities.

This module provides utilities for testing including test data generation,
mock helpers, assertion utilities, performance benchmarking, and fixture factories.
"""

# Import from submodules
from . import (
    assertion_helpers,
    benchmark_helpers,
    fixture_factories,
    mock_helpers,
    test_data_generators,
)

# Import all functions for direct access
from .assertion_helpers import (
    assert_almost_equal,
    assert_dict_contains,
    assert_in_range,
    assert_list_equal_unordered,
    assert_raises_with_message,
    assert_type_match,
)
from .benchmark_helpers import (
    benchmark_function,
    compare_functions,
    measure_memory_usage,
)
from .fixture_factories import (
    create_temp_dir_fixture,
    create_temp_file_fixture,
    mock_datetime_fixture,
)
from .mock_helpers import (
    create_mock_object,
    mock_api_response,
    mock_file_system,
)
from .test_data_generators import (
    generate_random_date,
    generate_random_datetime,
    generate_random_dict,
    generate_random_email,
    generate_random_float,
    generate_random_int,
    generate_random_list,
    generate_random_string,
    generate_random_url,
)

__all__ = [
    # Submodules
    "assertion_helpers",
    "benchmark_helpers",
    "fixture_factories",
    "mock_helpers",
    "test_data_generators",
    # Assertion helpers
    "assert_almost_equal",
    "assert_dict_contains",
    "assert_in_range",
    "assert_list_equal_unordered",
    "assert_raises_with_message",
    "assert_type_match",
    # Benchmark helpers
    "benchmark_function",
    "compare_functions",
    "measure_memory_usage",
    # Fixture factories
    "create_temp_dir_fixture",
    "create_temp_file_fixture",
    "mock_datetime_fixture",
    # Mock helpers
    "create_mock_object",
    "mock_api_response",
    "mock_file_system",
    # Test data generators
    "generate_random_date",
    "generate_random_datetime",
    "generate_random_dict",
    "generate_random_email",
    "generate_random_float",
    "generate_random_int",
    "generate_random_list",
    "generate_random_string",
    "generate_random_url",
]

