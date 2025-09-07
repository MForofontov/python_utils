import pytest
from typing import Any
from iterable_functions.dictionary_operations.deep_set import deep_set


def test_deep_set_case_1_basic_functionality() -> None:
    """
    Test case 1: Normal operation with basic deep set functionality.
    """
    # Arrange
    input_data: dict[str, Any] = {'user': {}}
    key_path: str = 'user.name'
    value: str = 'John'
    expected_output: dict[str, Any] = {'user': {'name': 'John'}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_2_list_of_keys() -> None:
    """
    Test case 2: Normal operation with list of keys.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: list[str] = ['user', 'profile', 'settings', 'theme']
    value: str = 'dark'
    expected_output: dict[str, Any] = {'user': {'profile': {'settings': {'theme': 'dark'}}}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_3_existing_nested_structure() -> None:
    """
    Test case 3: Normal operation on existing nested structure.
    """
    # Arrange
    input_data: dict[str, Any] = {'user': {'name': 'John'}}
    key_path: str = 'user.profile.age'
    value: int = 30
    expected_output: dict[str, Any] = {'user': {'name': 'John', 'profile': {'age': 30}}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_4_overwrite_existing_value() -> None:
    """
    Test case 4: Normal operation overwriting existing value.
    """
    # Arrange
    input_data: dict[str, Any] = {'user': {'name': 'John'}}
    key_path: str = 'user.name'
    value: str = 'Jane'
    expected_output: dict[str, Any] = {'user': {'name': 'Jane'}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_5_root_level_key() -> None:
    """
    Test case 5: Normal operation with root level key.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = 'name'
    value: str = 'John'
    expected_output: dict[str, Any] = {'name': 'John'}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_6_deeply_nested_structure() -> None:
    """
    Test case 6: Normal operation with deeply nested structure.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = 'level1.level2.level3.level4'
    value: str = 'value'
    expected_output: dict[str, Any] = {
        'level1': {
            'level2': {
                'level3': {
                    'level4': 'value'
                }
            }
        }
    }
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_7_mixed_data_types() -> None:
    """
    Test case 7: Normal operation with mixed data types.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    expected_output: dict[str, Any] = {
        'data': {
            'list': [1, 2, 3],
            'number': 42,
            'string': 'hello'
        }
    }
    
    # Act
    deep_set(input_data, 'data.list', [1, 2, 3])
    deep_set(input_data, 'data.number', 42)
    deep_set(input_data, 'data.string', 'hello')
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_8_invalid_type_error() -> None:
    """
    Test case 8: TypeError for invalid input type.
    """
    # Arrange
    invalid_input: str = "not a dict"
    key_path: str = 'key'
    value: str = 'value'
    expected_message: str = "d must be a dictionary, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        deep_set(invalid_input, key_path, value)


def test_deep_set_case_9_empty_string_in_path() -> None:
    """
    Test case 9: Edge case with empty string in path.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = '.nested'
    value: str = 'value'
    expected_output: dict[str, Any] = {'': {'nested': 'value'}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_10_single_key() -> None:
    """
    Test case 10: Edge case with single key.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = 'key'
    value: str = 'value'
    expected_output: dict[str, Any] = {'key': 'value'}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output


def test_deep_set_case_11_numeric_keys_in_path() -> None:
    """
    Test case 11: Normal operation with numeric keys in path.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = 'users.0.name'
    value: str = 'John'
    expected_output: dict[str, Any] = {'users': {'0': {'name': 'John'}}}
    
    # Act
    deep_set(input_data, key_path, value)
    
    # Assert
    assert input_data == expected_output
