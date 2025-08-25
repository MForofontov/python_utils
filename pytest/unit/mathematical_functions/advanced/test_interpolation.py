import pytest
from mathematical_functions.advanced.interpolation import interpolation


def test_interpolation_linear_basic() -> None:
    """
    Test case 1: Test basic linear interpolation.
    """
    x_data = [0, 1, 2, 3]
    y_data = [0, 2, 4, 6]
    x_new = [0.5, 1.5, 2.5]

    result = interpolation(x_data, y_data, x_new, method='linear')

    assert len(result['y_interpolated']) == 3
    assert abs(result['y_interpolated'][0] - 1.0) < 1e-10  # f(0.5) = 1
    assert abs(result['y_interpolated'][1] - 3.0) < 1e-10  # f(1.5) = 3
    assert abs(result['y_interpolated'][2] - 5.0) < 1e-10  # f(2.5) = 5
    assert result['method_used'] == 'linear'


def test_interpolation_polynomial_basic() -> None:
    """
    Test case 2: Test polynomial interpolation.
    """
    # Parabola y = x^2
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]
    x_new = [0.5, 1.5]

    result = interpolation(x_data, y_data, x_new, method='polynomial')

    # Should recover exact parabola
    assert abs(result['y_interpolated'][0] - 0.25) < 1e-10  # 0.5^2 = 0.25
    assert abs(result['y_interpolated'][1] - 2.25) < 1e-10  # 1.5^2 = 2.25


def test_interpolation_polynomial_degree() -> None:
    """
    Test case 16: Test polynomial degree parameter.
    """
    x_data = [0, 1, 2, 3, 4]
    y_data = [0, 1, 4, 9, 16]  # y = x^2
    x_new = [1.5]

    # Test different degrees
    result_2 = interpolation(x_data, y_data, x_new, method='polynomial', degree=2)

    # Should work with specified degree
    assert len(result_2['y_interpolated']) == 1
    assert isinstance(result_2['y_interpolated'][0], (int, float))


def test_interpolation_lagrange() -> None:
    """
    Test case 3: Test Lagrange interpolation.
    """
    x_data = [0, 1, 2]
    y_data = [1, 2, 5]  # y = x^2 + 1
    x_new = [0.5]

    result = interpolation(x_data, y_data, x_new, method='lagrange')

    # Should give approximately x^2 + 1 at x=0.5
    expected = 0.25 + 1  # 1.25
    assert abs(result['y_interpolated'][0] - expected) < 1e-10


def test_interpolation_newton() -> None:
    """
    Test case 4: Test Newton interpolation.
    """
    x_data = [0, 1, 2]
    y_data = [1, 1, 7]  # Quadratic polynomial
    x_new = [1.5]

    result = interpolation(x_data, y_data, x_new, method='newton')

    # Should interpolate correctly
    assert isinstance(result['y_interpolated'][0], (int, float))


def test_interpolation_cubic_spline() -> None:
    """
    Test case 5: Test cubic spline interpolation.
    """
    x_data = [0, 1, 2, 3]
    y_data = [0, 1, 4, 9]  # y = x^2
    x_new = [0.5, 1.5, 2.5]

    result = interpolation(x_data, y_data, x_new, method='cubic_spline')

    # Should be close to x^2 values
    assert len(result['y_interpolated']) == 3
    for val in result['y_interpolated']:
        assert isinstance(val, (int, float))


def test_interpolation_nearest_neighbor() -> None:
    """
    Test case 6: Test nearest neighbor interpolation.
    """
    x_data = [0, 2, 4]
    y_data = [10, 20, 30]
    x_new = [0.5, 1.5, 2.5, 3.5]

    result = interpolation(x_data, y_data, x_new, method='nearest_neighbor')

    # Should pick nearest values
    assert result['y_interpolated'][0] == 10  # Nearest to x=0
    assert result['y_interpolated'][1] == 20  # Nearest to x=2
    assert result['y_interpolated'][2] == 20  # Nearest to x=2
    assert result['y_interpolated'][3] == 30  # Nearest to x=4


def test_interpolation_extrapolation_allowed() -> None:
    """
    Test case 7: Test extrapolation when allowed.
    """
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]
    x_new = [-1, 3]  # Outside range

    result = interpolation(x_data, y_data, x_new, method='linear', extrapolate=True)

    assert len(result['y_interpolated']) == 2
    # Linear extrapolation should work
    assert isinstance(result['y_interpolated'][0], (int, float))
    assert isinstance(result['y_interpolated'][1], (int, float))


def test_interpolation_empty_x_new() -> None:
    """
    Test case 15: Test with empty x_new array.
    """
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]
    x_new = []

    result = interpolation(x_data, y_data, x_new, method='linear')

    assert len(result['y_interpolated']) == 0
    assert result['y_interpolated'] == []


def test_interpolation_return_structure() -> None:
    """
    Test case 17: Test that return structure is correct.
    """
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]
    x_new = [0.5]

    result = interpolation(x_data, y_data, x_new, method='linear')

    required_keys = ['y_interpolated', 'method_used', 'extrapolated_points', 'interpolation_error']
    for key in required_keys:
        assert key in result

    assert result['method_used'] == 'linear'
    assert isinstance(result['extrapolated_points'], list)


def test_interpolation_extrapolation_not_allowed() -> None:
    """
    Test case 8: Test that extrapolation raises error when not allowed.
    """
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]
    x_new = [-1, 3]  # Outside range

    with pytest.raises(ValueError, match="extrapolation not allowed"):
        interpolation(x_data, y_data, x_new, method='linear', extrapolate=False)


def test_interpolation_invalid_input_lengths() -> None:
    """
    Test case 9: Test error handling for invalid input lengths.
    """
    with pytest.raises(ValueError, match="x_data and y_data must have same length"):
        interpolation([0, 1], [0, 1, 2], [0.5], method='linear')


def test_interpolation_insufficient_data_points() -> None:
    """
    Test case 10: Test error handling for insufficient data points.
    """
    with pytest.raises(ValueError, match="At least 2 data points required"):
        interpolation([0], [1], [0.5], method='linear')


def test_interpolation_invalid_method() -> None:
    """
    Test case 11: Test error handling for invalid method.
    """
    with pytest.raises(ValueError, match="method must be one of"):
        interpolation([0, 1], [0, 1], [0.5], method='invalid_method')


def test_interpolation_type_errors() -> None:
    """
    Test case 12: Test type error handling.
    """
    with pytest.raises(TypeError, match="x_data must be a list"):
        interpolation("invalid", [0, 1], [0.5], method='linear')

    with pytest.raises(TypeError, match="y_data must be a list"):
        interpolation([0, 1], "invalid", [0.5], method='linear')

    with pytest.raises(TypeError, match="x_new must be a list"):
        interpolation([0, 1], [0, 1], "invalid", method='linear')


def test_interpolation_non_numeric_values() -> None:
    """
    Test case 13: Test error handling for non-numeric values.
    """
    with pytest.raises(TypeError, match="All values in x_data must be numeric"):
        interpolation([0, "1"], [0, 1], [0.5], method='linear')

    with pytest.raises(TypeError, match="All values in y_data must be numeric"):
        interpolation([0, 1], [0, "1"], [0.5], method='linear')

    with pytest.raises(TypeError, match="All values in x_new must be numeric"):
        interpolation([0, 1], [0, 1], [0.5, "1"], method='linear')


def test_interpolation_empty_arrays() -> None:
    """
    Test case 14: Test error handling for empty arrays.
    """
    with pytest.raises(ValueError, match="Input arrays cannot be empty"):
        interpolation([], [], [0.5], method='linear')


def test_interpolation_duplicate_x_values() -> None:
    """
    Test case 18: Test handling of duplicate x values.
    """
    x_data = [0, 1, 1, 2]  # Duplicate x=1
    y_data = [0, 1, 2, 4]
    x_new = [0.5]

    with pytest.raises(ValueError, match="Duplicate x values"):
        interpolation(x_data, y_data, x_new, method='linear')

