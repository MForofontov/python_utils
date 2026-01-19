import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.benchmark_helpers.measure_memory_usage import (
    measure_memory_usage,
)


def test_measure_memory_usage_simple_function() -> None:
    """
    Test case 1: Measure memory for simple function.
    """

    # Arrange
    def simple_func():
        return 42

    # Act
    result = measure_memory_usage(simple_func)

    # Assert
    assert "current_bytes" in result
    assert "peak_bytes" in result
    assert "result" in result
    assert result["result"] == 42


def test_measure_memory_usage_list_creation() -> None:
    """
    Test case 2: Measure memory for list creation.
    """

    # Arrange
    def create_list():
        return [i for i in range(1000)]

    # Act
    result = measure_memory_usage(create_list)

    # Assert
    assert result["peak_bytes"] > 0
    assert len(result["result"]) == 1000


def test_measure_memory_usage_dict_creation() -> None:
    """
    Test case 3: Measure memory for dict creation.
    """

    # Arrange
    def create_dict():
        return {i: i * 2 for i in range(500)}

    # Act
    result = measure_memory_usage(create_dict)

    # Assert
    assert result["peak_bytes"] > 0
    assert len(result["result"]) == 500


def test_measure_memory_usage_with_args() -> None:
    """
    Test case 4: Measure memory with function args.
    """

    # Arrange
    def multiply_list(n, factor):
        return [i * factor for i in range(n)]

    # Act
    result = measure_memory_usage(multiply_list, 100, 2)

    # Assert
    assert len(result["result"]) == 100
    assert result["peak_bytes"] >= 0


def test_measure_memory_usage_with_kwargs() -> None:
    """
    Test case 5: Measure memory with function kwargs.
    """

    # Arrange
    def create_dict(size=10, prefix="key"):
        return {f"{prefix}_{i}": i for i in range(size)}

    # Act
    result = measure_memory_usage(create_dict, size=50, prefix="test")

    # Assert
    assert len(result["result"]) == 50


def test_measure_memory_usage_type_error_func() -> None:
    """
    Test case 6: TypeError for non-callable func.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="func must be callable"):
        measure_memory_usage("not callable")
