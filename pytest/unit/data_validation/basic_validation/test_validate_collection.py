import pytest

pytestmark = [pytest.mark.unit, pytest.mark.data_validation]
from data_validation import validate_collection


def test_validate_collection_basic_collections() -> None:
    """
    Test case 1: Basic collection type validation.
    """
    # Test list
    validate_collection([1, 2, 3], list)
    validate_collection([], list)

    # Test tuple
    validate_collection((1, 2, 3), tuple)
    validate_collection((), tuple)

    # Test set
    validate_collection({1, 2, 3}, set)
    validate_collection(set(), set)

    # Test dict
    validate_collection({"a": 1, "b": 2}, dict)
    validate_collection({}, dict)


def test_validate_collection_length_validation() -> None:
    """
    Test case 2: Collection length validation with min/max bounds.
    """
    # Test minimum length
    validate_collection([1, 2, 3], list, min_length=2)
    validate_collection([1, 2], list, min_length=2)

    # Test maximum length
    validate_collection([1, 2, 3], list, max_length=5)
    validate_collection([1, 2, 3], list, max_length=3)

    # Test both min and max length
    validate_collection([1, 2, 3], list, min_length=2, max_length=5)
    validate_collection({"a": 1, "b": 2, "c": 3}, dict, min_length=2, max_length=5)


def test_validate_collection_empty_collection_handling() -> None:
    """
    Test case 3: Empty collection handling with allow_empty parameter.
    """
    # Test allow_empty=True (default)
    validate_collection([], list, allow_empty=True)
    validate_collection({}, dict, allow_empty=True)
    validate_collection(set(), set, allow_empty=True)
    validate_collection((), tuple, allow_empty=True)

    # Test with length constraints and empty allowed
    validate_collection([], list, min_length=0, max_length=5, allow_empty=True)


def test_validate_collection_element_type_validation() -> None:
    """
    Test case 4: Element type validation for homogeneous collections.
    """
    # Test list with integer elements
    validate_collection([1, 2, 3], list, element_type=int)

    # Test list with string elements
    validate_collection(["a", "b", "c"], list, element_type=str)

    # Test set with float elements
    validate_collection({1.1, 2.2, 3.3}, set, element_type=float)

    # Test tuple with boolean elements
    validate_collection((True, False, True), tuple, element_type=bool)


def test_validate_collection_dict_value_validation() -> None:
    """
    Test case 5: Dictionary value type validation.
    """
    # Test dict with integer values
    validate_collection({"a": 1, "b": 2, "c": 3}, dict, element_type=int)

    # Test dict with string values
    validate_collection({"key1": "value1", "key2": "value2"}, dict, element_type=str)

    # Test dict with mixed valid types
    validate_collection({"a": 1, "b": "hello"}, dict, element_type=(int, str))


def test_validate_collection_union_element_types() -> None:
    """
    Test case 6: Union element type validation.
    """
    # Test list with int or str elements
    validate_collection([1, "hello", 2, "world"], list, element_type=(int, str))

    # Test set with multiple allowed types
    validate_collection({1, 2.5, "text"}, set, element_type=(int, float, str))

    # Test tuple with boolean or int (bool is subclass of int in Python)
    validate_collection((True, 1, False, 0), tuple, element_type=(bool, int))


def test_validate_collection_complex_validation_combinations() -> None:
    """
    Test case 7: Complex combinations of validation parameters.
    """
    # Test all parameters together
    validate_collection(
        [1, 2, 3, 4],
        list,
        min_length=3,
        max_length=5,
        allow_empty=False,
        element_type=int,
    )

    # Test dict with all parameters
    validate_collection(
        {"a": 1, "b": 2},
        dict,
        min_length=1,
        max_length=3,
        allow_empty=False,
        element_type=int,
    )


def test_validate_collection_edge_cases() -> None:
    """
    Test case 8: Edge cases and boundary conditions.
    """
    # Test single element collections
    validate_collection([1], list, min_length=1, max_length=1, element_type=int)
    validate_collection({"a": 1}, dict, min_length=1, max_length=1, element_type=int)

    # Test large collections
    large_list = list(range(10000))
    validate_collection(large_list, list, element_type=int)

    # Test nested collections (without element type checking)
    nested_list = [[1, 2], [3, 4], [5, 6]]
    validate_collection(nested_list, list)

    # Test collections with None elements
    validate_collection([1, None, 3], list, element_type=(int, type(None)))


def test_validate_collection_performance_large_collections() -> None:
    """
    Test case 9: Performance with large collections.
    """
    # Test large collection without element validation (should be fast)
    large_list = list(range(100000))
    import time

    start_time = time.time()
    validate_collection(large_list, list, min_length=1000, max_length=200000)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 0.1  # Should be very fast without element checking

    # Test smaller collection with element validation
    medium_list = list(range(10000))
    start_time = time.time()
    validate_collection(medium_list, list, element_type=int)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 1.0  # Should complete within 1 second


def test_validate_collection_type_error_wrong_collection_type() -> None:
    """
    Test case 10: TypeError for wrong collection type.
    """
    with pytest.raises(TypeError, match="collection must be list, got tuple"):
        validate_collection((1, 2, 3), list)

    with pytest.raises(TypeError, match="collection must be dict, got list"):
        validate_collection([1, 2, 3], dict)

    with pytest.raises(TypeError, match="collection must be set, got list"):
        validate_collection([1, 2, 3], set)

    # Test with custom param name
    with pytest.raises(TypeError, match="items must be list, got str"):
        validate_collection("not a list", list, param_name="items")


def test_validate_collection_value_error_empty_not_allowed() -> None:
    """
    Test case 11: ValueError when empty collections are not allowed.
    """
    with pytest.raises(ValueError, match="collection cannot be empty"):
        validate_collection([], list, allow_empty=False)

    with pytest.raises(ValueError, match="collection cannot be empty"):
        validate_collection({}, dict, allow_empty=False)

    with pytest.raises(ValueError, match="collection cannot be empty"):
        validate_collection(set(), set, allow_empty=False)

    # Test with custom param name
    with pytest.raises(ValueError, match="items cannot be empty"):
        validate_collection([], list, allow_empty=False, param_name="items")


def test_validate_collection_value_error_length_bounds() -> None:
    """
    Test case 12: ValueError for length constraint violations.
    """
    # Test below minimum length
    with pytest.raises(
        ValueError,
        match="collection length \\(1\\) is below minimum allowed length \\(3\\)",
    ):
        validate_collection([1], list, min_length=3)

    # Test above maximum length
    with pytest.raises(
        ValueError,
        match="collection length \\(5\\) exceeds maximum allowed length \\(3\\)",
    ):
        validate_collection([1, 2, 3, 4, 5], list, max_length=3)

    # Test with custom param name
    with pytest.raises(
        ValueError, match="items length \\(2\\) is below minimum allowed length \\(5\\)"
    ):
        validate_collection([1, 2], list, min_length=5, param_name="items")


def test_validate_collection_type_error_element_validation() -> None:
    """
    Test case 13: TypeError for wrong element types.
    """
    # Test wrong single element type
    with pytest.raises(
        TypeError, match="collection element at index 1 must be int, got str"
    ):
        validate_collection([1, "hello", 3], list, element_type=int)

    # Test wrong union element type
    with pytest.raises(
        TypeError, match="collection element at index 2 must be int \\| str, got float"
    ):
        validate_collection([1, "hello", 3.14], list, element_type=(int, str))

    # Test dict value type error
    with pytest.raises(
        TypeError, match="collection value for key 'b' must be int, got str"
    ):
        validate_collection({"a": 1, "b": "hello"}, dict, element_type=int)

    # Test with custom param name
    with pytest.raises(
        TypeError, match="items element at index 0 must be str, got int"
    ):
        validate_collection([1, 2, 3], list, element_type=str, param_name="items")


def test_validate_collection_type_error_invalid_parameters() -> None:
    """
    Test case 14: TypeError for invalid parameter types.
    """
    # Test invalid expected_type
    with pytest.raises(TypeError, match="expected_type must be a type"):
        validate_collection([1, 2, 3], "list")

    # Test invalid min_length
    with pytest.raises(TypeError, match="min_length must be int or None, got str"):
        validate_collection([1, 2, 3], list, min_length="5")

    # Test invalid max_length
    with pytest.raises(TypeError, match="max_length must be int or None, got float"):
        validate_collection([1, 2, 3], list, max_length=5.5)

    # Test invalid allow_empty
    with pytest.raises(TypeError, match="allow_empty must be bool, got str"):
        validate_collection([1, 2, 3], list, allow_empty="true")

    # Test negative lengths
    with pytest.raises(ValueError, match="min_length must be non-negative, got -1"):
        validate_collection([1, 2, 3], list, min_length=-1)

    with pytest.raises(ValueError, match="max_length must be non-negative, got -1"):
        validate_collection([1, 2, 3], list, max_length=-1)

    # Test min_length > max_length
    with pytest.raises(
        ValueError, match="min_length \\(5\\) cannot be greater than max_length \\(3\\)"
    ):
        validate_collection([1, 2, 3], list, min_length=5, max_length=3)


def test_validate_collection_allow_empty_type_error() -> None:
    """Test case 15: Test TypeError for non-bool allow_empty parameter."""
    with pytest.raises(TypeError, match="allow_empty must be bool"):
        validate_collection([1, 2, 3], list, allow_empty=1)  # type: ignore


def test_validate_collection_max_length_type_error() -> None:
    """Test case 16: Test TypeError for non-integer max_length parameter."""
    with pytest.raises(TypeError, match="max_length must be int or None"):
        validate_collection([1, 2, 3], list, max_length="10")  # type: ignore


def test_validate_collection_non_iterable_element_validation() -> None:
    """Test case 17: Test TypeError for non-iterable with element_type validation."""

    # Create a custom class that is Sized but not Iterable to trigger line 159
    class SizedNotIterable:
        def __len__(self) -> int:
            return 5

    obj = SizedNotIterable()
    with pytest.raises(TypeError, match="must be iterable for element type validation"):
        validate_collection(obj, SizedNotIterable, element_type=int)  # type: ignore


def test_validate_collection_dict_element_validation_failure() -> None:
    """Test case 18: Test element type validation for dictionary values."""
    with pytest.raises(TypeError, match="value for key 'b' must be int"):
        validate_collection({"a": 1, "b": "two"}, dict, element_type=int)
