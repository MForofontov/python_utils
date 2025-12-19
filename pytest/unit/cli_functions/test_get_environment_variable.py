import os

import pytest
from cli_functions.get_environment_variable import get_environment_variable


def test_get_environment_variable_case_1_existing_variable() -> None:
    """
    Test case 1: Get existing environment variable.
    """
    os.environ['TEST_VAR'] = 'test_value'
    try:
        result = get_environment_variable('TEST_VAR')
        assert result == 'test_value'
    finally:
        del os.environ['TEST_VAR']


def test_get_environment_variable_case_2_nonexistent_with_default() -> None:
    """
    Test case 2: Get nonexistent variable with default value.
    """
    result = get_environment_variable('NONEXISTENT_VAR', default='default_value')
    assert result == 'default_value'


def test_get_environment_variable_case_3_nonexistent_without_default() -> None:
    """
    Test case 3: Get nonexistent variable without default returns None.
    """
    result = get_environment_variable('NONEXISTENT_VAR')
    assert result is None


def test_get_environment_variable_case_4_required_missing_error() -> None:
    """
    Test case 4: Required variable that is missing raises ValueError.
    """
    with pytest.raises(ValueError, match="Required environment variable"):
        get_environment_variable('NONEXISTENT_REQUIRED_VAR', required=True)


def test_get_environment_variable_case_5_invalid_type_error() -> None:
    """
    Test case 5: Invalid var_name type raises TypeError.
    """
    with pytest.raises(TypeError, match="var_name must be a string"):
        get_environment_variable(123)
    
    with pytest.raises(TypeError):
        get_environment_variable(None)


def test_get_environment_variable_case_6_required_existing() -> None:
    """
    Test case 6: Required variable that exists returns value.
    """
    os.environ['TEST_REQUIRED'] = 'required_value'
    try:
        result = get_environment_variable('TEST_REQUIRED', required=True)
        assert result == 'required_value'
    finally:
        del os.environ['TEST_REQUIRED']
