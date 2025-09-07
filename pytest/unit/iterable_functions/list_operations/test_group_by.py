import pytest
from typing import Any, List
from iterable_functions.list_operations.group_by import group_by


def test_group_by_case_1_group_by_length() -> None:
    """
    Test case 1: Normal operation grouping strings by length.
    """
    # Arrange
    input_items: List[str] = ['cat', 'dog', 'bird', 'elephant']
    key_function = lambda x: len(x)
    expected_output = {3: ['cat', 'dog'], 4: ['bird'], 8: ['elephant']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_2_group_by_first_character() -> None:
    """
    Test case 2: Normal operation grouping by first character.
    """
    # Arrange
    input_items: List[str] = ['cat', 'dog', 'bird', 'elephant']
    key_function = lambda x: x[0]
    expected_output = {'c': ['cat'], 'd': ['dog'], 'b': ['bird'], 'e': ['elephant']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_3_group_numbers_by_parity() -> None:
    """
    Test case 3: Normal operation grouping numbers by even/odd.
    """
    # Arrange
    input_items: List[int] = [1, 2, 3, 4, 5, 6]
    key_function = lambda x: 'even' if x % 2 == 0 else 'odd'
    expected_output = {'odd': [1, 3, 5], 'even': [2, 4, 6]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_4_group_duplicates_without_key_function() -> None:
    """
    Test case 4: Normal operation grouping duplicates without key function.
    """
    # Arrange
    input_items: List[str] = ['a', 'b', 'a', 'c', 'b']
    expected_output = {'a': ['a', 'a'], 'b': ['b', 'b'], 'c': ['c']}

    # Act
    result = group_by(input_items)

    # Assert
    assert result == expected_output


def test_group_by_case_5_empty_list() -> None:
    """
    Test case 5: Edge case with empty list.
    """
    # Arrange
    input_items: List[str] = []
    key_function = lambda x: len(x)
    expected_output = {}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_6_single_item_list() -> None:
    """
    Test case 6: Edge case with single item list.
    """
    # Arrange
    input_items: List[str] = ['hello']
    key_function = lambda x: len(x)
    expected_output = {5: ['hello']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_7_mixed_data_types() -> None:
    """
    Test case 7: Normal operation with mixed data types.
    """
    # Arrange
    input_items: List[Any] = [1, 'hello', 2, 'world', 1]
    key_function = lambda x: type(x).__name__
    expected_output = {'int': [1, 2, 1], 'str': ['hello', 'world']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_case_8_complex_objects() -> None:
    """
    Test case 8: Normal operation with complex objects.
    """
    # Arrange
    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    people = [
        Person('Alice', 25),
        Person('Bob', 30),
        Person('Charlie', 25),
        Person('David', 30)
    ]
    key_function = lambda p: p.age
    expected_output = {
        25: [people[0], people[2]],
        30: [people[1], people[3]]
    }

    # Act
    result = group_by(people, key_function)

    # Assert
    assert len(result[25]) == 2
    assert len(result[30]) == 2
    assert all(p.age == 25 for p in result[25])
    assert all(p.age == 30 for p in result[30])


def test_group_by_case_9_invalid_items_type_error() -> None:
    """
    Test case 9: TypeError for invalid items type.
    """
    # Arrange
    invalid_items: str = "not a list"
    key_function = lambda x: x
    expected_message: str = "items must be a list, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        group_by(invalid_items, key_function)  # type: ignore


def test_group_by_case_10_invalid_key_func_type_error() -> None:
    """
    Test case 10: TypeError for invalid key_func type.
    """
    # Arrange
    input_items: List[str] = ['a', 'b', 'c']
    invalid_key_func: str = "not callable"
    expected_message: str = "key_func must be callable or None, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        group_by(input_items, invalid_key_func)  # type: ignore


def test_group_by_case_11_preserves_order() -> None:
    """
    Test case 11: Verify that original order is preserved within groups.
    """
    # Arrange
    input_items: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']
    key_function = lambda x: len(x)
    expected_output = {5: ['first', 'third', 'fifth'], 6: ['second', 'fourth']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output
    # Verify order is preserved
    assert result[5] == ['first', 'third', 'fifth']
    assert result[6] == ['second', 'fourth']


def test_group_by_case_12_none_values() -> None:
    """
    Test case 12: Normal operation with None values.
    """
    # Arrange
    input_items: List[Any] = [None, 'a', None, 'b']
    key_function = lambda x: x
    expected_output = {None: [None, None], 'a': ['a'], 'b': ['b']}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output
