import pytest
from testing_functions.test_data_generators.generate_random_dict import (
    generate_random_dict,
)


def test_generate_random_dict_case_1_default_parameters() -> None:
    """
    Test case 1: Generate random dict with default parameters.
    """
    # Act
    result = generate_random_dict()
    
    # Assert
    assert isinstance(result, dict)
    assert len(result) == 5
    assert all(k.startswith("key_") for k in result.keys())
    assert all(isinstance(v, int) for v in result.values())


def test_generate_random_dict_case_2_custom_num_keys() -> None:
    """
    Test case 2: Generate random dict with custom number of keys.
    """
    # Act
    result = generate_random_dict(3)
    
    # Assert
    assert len(result) == 3


def test_generate_random_dict_case_3_custom_key_prefix() -> None:
    """
    Test case 3: Generate random dict with custom key prefix.
    """
    # Act
    result = generate_random_dict(5, "test")
    
    # Assert
    assert all(k.startswith("test_") for k in result.keys())


def test_generate_random_dict_case_4_float_values() -> None:
    """
    Test case 4: Generate random dict with float values.
    """
    # Act
    result = generate_random_dict(5, "key", "float")
    
    # Assert
    assert all(isinstance(v, float) for v in result.values())


def test_generate_random_dict_case_5_string_values() -> None:
    """
    Test case 5: Generate random dict with string values.
    """
    # Act
    result = generate_random_dict(5, "key", "str")
    
    # Assert
    assert all(isinstance(v, str) for v in result.values())


def test_generate_random_dict_case_6_empty_dict() -> None:
    """
    Test case 6: Generate empty dict.
    """
    # Act
    result = generate_random_dict(0)
    
    # Assert
    assert result == {}


def test_generate_random_dict_case_7_type_error_num_keys() -> None:
    """
    Test case 7: TypeError for invalid num_keys type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="num_keys must be an integer"):
        generate_random_dict("5")


def test_generate_random_dict_case_8_type_error_key_prefix() -> None:
    """
    Test case 8: TypeError for invalid key_prefix type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="key_prefix must be a string"):
        generate_random_dict(5, 123)


def test_generate_random_dict_case_9_type_error_value_type() -> None:
    """
    Test case 9: TypeError for invalid value_type type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="value_type must be a string"):
        generate_random_dict(5, "key", 123)


def test_generate_random_dict_case_10_value_error_negative_num_keys() -> None:
    """
    Test case 10: ValueError for negative num_keys.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="num_keys must be non-negative"):
        generate_random_dict(-1)


def test_generate_random_dict_case_11_value_error_invalid_value_type() -> None:
    """
    Test case 11: ValueError for invalid value_type value.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="value_type must be 'int', 'float', or 'str'"):
        generate_random_dict(5, "key", "boolean")
