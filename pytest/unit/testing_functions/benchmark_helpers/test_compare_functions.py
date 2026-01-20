import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from pyutils_collection.testing_functions.benchmark_helpers.compare_functions import compare_functions


def test_compare_functions_equal_functions() -> None:
    """
    Test case 1: Compare two similar functions.
    """

    # Arrange
    def func_a(x):
        return x * 2

    def func_b(x):
        return x + x

    # Act
    result = compare_functions(func_a, func_b, (5,), (5,), iterations=10)

    # Assert
    assert "func1_avg_time" in result
    assert "func2_avg_time" in result
    assert "speedup" in result
    assert "faster_function" in result
    assert result["faster_function"] in ["func1", "func2"]


def test_compare_functions_different_args() -> None:
    """
    Test case 2: Compare functions with different arguments.
    """

    # Arrange
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    # Act
    result = compare_functions(add, multiply, (1, 2), (3, 4), iterations=10)

    # Assert
    assert result["func1_avg_time"] >= 0
    assert result["func2_avg_time"] >= 0


def test_compare_functions_speedup_calculation() -> None:
    """
    Test case 3: Verify speedup calculation.
    """

    # Arrange
    def fast_func():
        return 1

    def slow_func():
        sum(range(1000))
        return 1

    # Act
    result = compare_functions(fast_func, slow_func, (), (), iterations=10)

    # Assert
    assert result["speedup"] > 0


def test_compare_functions_single_iteration() -> None:
    """
    Test case 4: Compare with single iteration.
    """

    # Arrange
    def func1():
        return 1

    def func2():
        return 2

    # Act
    result = compare_functions(func1, func2, (), (), iterations=1)

    # Assert
    assert result["func1_total_time"] == result["func1_avg_time"]
    assert result["func2_total_time"] == result["func2_avg_time"]


def test_compare_functions_type_error_func1() -> None:
    """
    Test case 5: TypeError for non-callable func1.
    """

    # Arrange
    def func2():
        return 1

    # Act & Assert
    with pytest.raises(TypeError, match="func1 must be callable"):
        compare_functions("not callable", func2)


def test_compare_functions_type_error_func2() -> None:
    """
    Test case 6: TypeError for non-callable func2.
    """

    # Arrange
    def func1():
        return 1

    # Act & Assert
    with pytest.raises(TypeError, match="func2 must be callable"):
        compare_functions(func1, "not callable")


def test_compare_functions_type_error_args1() -> None:
    """
    Test case 7: TypeError for invalid args1 type.
    """

    # Arrange
    def func1():
        return 1

    def func2():
        return 1

    # Act & Assert
    with pytest.raises(TypeError, match="args1 must be a tuple"):
        compare_functions(func1, func2, [1, 2], ())


def test_compare_functions_type_error_args2() -> None:
    """
    Test case 8: TypeError for invalid args2 type.
    """

    # Arrange
    def func1():
        return 1

    def func2():
        return 1

    # Act & Assert
    with pytest.raises(TypeError, match="args2 must be a tuple"):
        compare_functions(func1, func2, (), [1, 2])


def test_compare_functions_type_error_iterations() -> None:
    """
    Test case 9: TypeError for invalid iterations type.
    """

    # Arrange
    def func1():
        return 1

    def func2():
        return 1

    # Act & Assert
    with pytest.raises(TypeError, match="iterations must be an integer"):
        compare_functions(func1, func2, (), (), iterations="10")


def test_compare_functions_value_error_iterations() -> None:
    """
    Test case 10: ValueError for invalid iterations value.
    """

    # Arrange
    def func1():
        return 1

    def func2():
        return 1

    # Act & Assert
    with pytest.raises(ValueError, match="iterations must be positive"):
        compare_functions(func1, func2, (), (), iterations=0)
