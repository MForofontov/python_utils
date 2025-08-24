import pytest
import os
from env_config_functions.get_env_var import get_env_var

def test_get_env_var_basic(monkeypatch):
    """
    Test case 1: Get env var as string
    """
    monkeypatch.setenv('FOO', 'bar')
    assert get_env_var('FOO') == 'bar'

def test_get_env_var_default(monkeypatch):
    """
    Test case 2: Get env var with default
    """
    assert get_env_var('NOT_SET', default='baz') == 'baz'

def test_get_env_var_cast_int(monkeypatch):
    """
    Test case 3: Get env var with int cast
    """
    monkeypatch.setenv('PORT', '8080')
    assert get_env_var('PORT', cast=int) == 8080

def test_get_env_var_cast_fail(monkeypatch):
    """
    Test case 4: Casting failure raises ValueError
    """
    monkeypatch.setenv('PORT', 'not_an_int')
    with pytest.raises(ValueError):
        get_env_var('PORT', cast=int)
