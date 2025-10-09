import pytest
from data_validation import validate_type


def test_validate_type_basic_types() -> None:
    """
    Test case 1: Basic type validation with common Python types.
    """
    # Test int
    validate_type(42, int)

    # Test str
    validate_type("hello", str)

    # Test float
    validate_type(3.14, float)

    # Test bool
    validate_type(True, bool)

    # Test list
    validate_type([1, 2, 3], list)

    # Test dict
    validate_type({"key": "value"}, dict)

    # Test set
    validate_type({1, 2, 3}, set)

    # Test tuple
    validate_type((1, 2, 3), tuple)


def test_validate_type_union_types() -> None:
    """
    Test case 2: Union type validation with multiple acceptable types.
    """
    # Test int or str
    validate_type(42, (int, str))
    validate_type("hello", (int, str))

    # Test multiple types
    validate_type([1, 2], (list, tuple, set))
    validate_type((1, 2), (list, tuple, set))
    validate_type({1, 2}, (list, tuple, set))

    # Test with None in union
    validate_type(42, (int, type(None)))
    validate_type(None, (int, type(None)))


def test_validate_type_none_handling() -> None:
    """
    Test case 3: None value handling with allow_none parameter.
    """
    # Test allow_none=True
    validate_type(None, str, allow_none=True)
    validate_type(None, int, allow_none=True)
    validate_type(None, (int, str), allow_none=True)

    # Test normal values with allow_none=True
    validate_type("hello", str, allow_none=True)
    validate_type(42, int, allow_none=True)


def test_validate_type_custom_param_name() -> None:
    """
    Test case 4: Custom parameter name in error messages.
    """
    # Test with custom param name
    validate_type(42, int, param_name="user_id")
    validate_type("test", str, param_name="username")


def test_validate_type_type_error_single_type() -> None:
    """
    Test case 5: TypeError for wrong type with single expected type.
    """
    with pytest.raises(TypeError, match="value must be str, got int"):
        validate_type(42, str)

    with pytest.raises(TypeError, match="value must be int, got str"):
        validate_type("hello", int)

    with pytest.raises(TypeError, match="value must be list, got dict"):
        validate_type({"key": "value"}, list)

    # Test with custom param name
    with pytest.raises(TypeError, match="user_id must be int, got str"):
        validate_type("123", int, param_name="user_id")


def test_validate_type_type_error_union_types() -> None:
    """
    Test case 6: TypeError for wrong type with union types.
    """
    with pytest.raises(TypeError, match="value must be int \\| str, got float"):
        validate_type(3.14, (int, str))

    with pytest.raises(TypeError, match="value must be list \\| tuple, got set"):
        validate_type({1, 2, 3}, (list, tuple))

    # Test with custom param name
    with pytest.raises(TypeError, match="data must be dict \\| list, got str"):
        validate_type("invalid", (dict, list), param_name="data")


def test_validate_type_none_not_allowed() -> None:
    """
    Test case 7: TypeError when None is not allowed.
    """
    with pytest.raises(TypeError, match="value cannot be None, expected str"):
        validate_type(None, str)

    with pytest.raises(TypeError, match="value cannot be None, expected int"):
        validate_type(None, int, allow_none=False)

    with pytest.raises(TypeError, match="value cannot be None, expected int \\| str"):
        validate_type(None, (int, str))

    # Test with custom param name
    with pytest.raises(TypeError, match="user_id cannot be None, expected int"):
        validate_type(None, int, param_name="user_id")


def test_validate_type_complex_collections() -> None:
    """
    Test case 8: Validation with complex collection types.
    """
    # Test nested structures
    validate_type({"users": [1, 2, 3]}, dict)
    validate_type([{"name": "John"}, {"name": "Jane"}], list)
    validate_type(({1, 2}, {3, 4}), tuple)

    # Test empty collections
    validate_type([], list)
    validate_type({}, dict)
    validate_type(set(), set)
    validate_type((), tuple)


def test_validate_type_edge_cases() -> None:
    """
    Test case 9: Edge cases and boundary conditions.
    """
    # Test with zero values
    validate_type(0, int)
    validate_type(0.0, float)
    validate_type("", str)
    validate_type(False, bool)

    # Test with large collections
    large_list = list(range(10000))
    validate_type(large_list, list)

    # Test inheritance (bool is subclass of int in Python)
    validate_type(True, int)  # Should pass since bool inherits from int
    validate_type(False, int)  # Should pass since bool inherits from int


def test_validate_type_performance_large_unions() -> None:
    """
    Test case 10: Performance with large union types.
    """
    # Test with many union types
    many_types = (int, str, float, bool, list, dict, set, tuple, bytes, bytearray)

    validate_type(42, many_types)
    validate_type("hello", many_types)
    validate_type([1, 2, 3], many_types)

    # Should be fast even with many types
    import time

    start_time = time.time()
    for _ in range(1000):
        validate_type(42, many_types)
    elapsed_time = time.time() - start_time

    assert elapsed_time < 1.0  # Should complete within 1 second
