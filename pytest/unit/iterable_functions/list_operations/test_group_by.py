import pytest
from typing import Any
from iterable_functions.list_operations.group_by import group_by


def test_group_by_group_by_length() -> None:
    """
    Test case 1: Group strings by length.
    """
    # Arrange
    input_items: list[str] = ["cat", "dog", "bird", "elephant"]

    def key_function(x):
        return len(x)

    expected_output = {3: ["cat", "dog"], 4: ["bird"], 8: ["elephant"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_group_by_first_character() -> None:
    """
    Test case 2: Group strings by first character.
    """
    # Arrange
    input_items: list[str] = ["cat", "dog", "bird", "elephant"]

    def key_function(x):
        return x[0]

    expected_output = {"c": ["cat"], "d": ["dog"], "b": ["bird"], "e": ["elephant"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_group_numbers_by_parity() -> None:
    """
    Test case 3: Group numbers by even/odd parity.
    """
    # Arrange
    input_items: list[int] = [1, 2, 3, 4, 5, 6]

    def key_function(x):
        return "even" if x % 2 == 0 else "odd"

    expected_output = {"odd": [1, 3, 5], "even": [2, 4, 6]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_group_duplicates_without_key_function() -> None:
    """
    Test case 4: Group duplicates without key function.
    """
    # Arrange
    input_items: list[str] = ["a", "b", "a", "c", "b"]
    expected_output = {"a": ["a", "a"], "b": ["b", "b"], "c": ["c"]}

    # Act
    result = group_by(input_items)

    # Assert
    assert result == expected_output


def test_group_by_empty_list() -> None:
    """
    Test case 5: Edge case with empty list.
    """
    # Arrange
    input_items: list[str] = []

    def key_function(x):
        return len(x)

    expected_output = {}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_single_item_list() -> None:
    """
    Test case 6: Edge case with single item list.
    """
    # Arrange
    input_items: list[str] = ["hello"]

    def key_function(x):
        return len(x)

    expected_output = {5: ["hello"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_mixed_data_types() -> None:
    """
    Test case 7: Group mixed data types.
    """
    # Arrange
    input_items: list[Any] = [1, "hello", 2, "world", 1]

    def key_function(x):
        return type(x).__name__

    expected_output = {"int": [1, 2, 1], "str": ["hello", "world"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output


def test_group_by_complex_objects() -> None:
    """
    Test case 8: Group complex objects by attribute.
    """

    # Arrange
    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    people = [
        Person("Alice", 25),
        Person("Bob", 30),
        Person("Charlie", 25),
        Person("David", 30),
    ]

    def key_function(p):
        return p.age

    {25: [people[0], people[2]], 30: [people[1], people[3]]}

    # Act
    result = group_by(people, key_function)

    # Assert
    assert len(result[25]) == 2
    assert len(result[30]) == 2
    assert all(p.age == 25 for p in result[25])
    assert all(p.age == 30 for p in result[30])


def test_group_by_invalid_items_type_error() -> None:
    """
    Test case 9: TypeError for invalid items type.
    """
    # Arrange
    invalid_items: str = "not a list"

    def key_function(x):
        return x

    expected_message: str = "items must be a list, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        group_by(invalid_items, key_function)  # type: ignore


def test_group_by_invalid_key_func_type_error() -> None:
    """
    Test case 10: TypeError for invalid key_func type.
    """
    # Arrange
    input_items: list[str] = ["a", "b", "c"]
    invalid_key_func: str = "not callable"
    expected_message: str = "key_func must be callable or None, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        group_by(input_items, invalid_key_func)  # type: ignore


def test_group_by_preserves_order() -> None:
    """
    Test case 11: Preserve original order within groups.
    """
    # Arrange
    input_items: list[str] = ["first", "second", "third", "fourth", "fifth"]

    def key_function(x):
        return len(x)

    expected_output = {5: ["first", "third", "fifth"], 6: ["second", "fourth"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output
    # Verify order is preserved
    assert result[5] == ["first", "third", "fifth"]
    assert result[6] == ["second", "fourth"]


def test_group_by_none_values() -> None:
    """
    Test case 12: Group None values.
    """
    # Arrange
    input_items: list[Any] = [None, "a", None, "b"]

    def key_function(x):
        return x

    expected_output = {None: [None, None], "a": ["a"], "b": ["b"]}

    # Act
    result = group_by(input_items, key_function)

    # Assert
    assert result == expected_output
