import pytest
from env_config_functions.expand_env_vars_in_string import expand_env_vars_in_string

def test_expand_env_vars_basic(monkeypatch):
    """
    Test case 1: Expand $VAR and ${VAR} in string
    """
    monkeypatch.setenv('FOO', 'bar')
    monkeypatch.setenv('USER', 'alice')
    s = 'User: $USER, Foo: ${FOO}'
    result = expand_env_vars_in_string(s)
    assert result == 'User: alice, Foo: bar'

def test_expand_env_vars_missing(monkeypatch):
    """
    Test case 2: Missing variable replaced with empty string
    """
    s = 'Path: $NOT_SET'
    result = expand_env_vars_in_string(s)
    assert result == 'Path: '

def test_expand_env_vars_with_default(monkeypatch):
    """
    Test case 3: Missing variable replaced with default
    """
    s = 'Path: $NOT_SET'
    result = expand_env_vars_in_string(s, default='none')
    assert result == 'Path: none'

def test_expand_env_vars_multiple(monkeypatch):
    """
    Test case 4: Multiple variables in string
    """
    monkeypatch.setenv('A', '1')
    monkeypatch.setenv('B', '2')
    s = '$A-$B-$C'
    result = expand_env_vars_in_string(s, default='x')
    assert result == '1-2-x'


def test_expand_env_vars_empty_string():
    """
    Test case 5: Empty string input
    """
    result = expand_env_vars_in_string('')
    assert result == ''


def test_expand_env_vars_no_variables():
    """
    Test case 6: String with no variables
    """
    s = 'No variables here'
    result = expand_env_vars_in_string(s)
    assert result == 'No variables here'


def test_expand_env_vars_invalid_string_type():
    """
    Test case 7: Test with invalid string type
    """
    with pytest.raises(TypeError):
        expand_env_vars_in_string(123)


def test_expand_env_vars_invalid_string_none():
    """
    Test case 8: Test with None input
    """
    with pytest.raises(TypeError):
        expand_env_vars_in_string(None)


def test_expand_env_vars_invalid_default_type():
    """
    Test case 9: Test with invalid default type
    """
    with pytest.raises(TypeError):
        expand_env_vars_in_string('$VAR', default=123)
