import os
import pytest
import logging
from decorators.env_config import env_config

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

# Sample function to be decorated
@env_config('TEST_ENV_VAR')
def sample_function(env_var_value=None):
    return f"Function executed with env_var_value: {env_var_value}"

@env_config('TEST_ENV_VAR', logger=test_logger, default='default_value', required=False, var_type=str, custom_message="Custom log message")
def sample_function_logger(env_var_value=None):
    return f"Function executed with env_var_value: {env_var_value}"

def test_env_var_set(monkeypatch, capsys):
    """
    Test case 1: Environment variable is set with default message, no logger provided
    """
    # Test case 1: Environment variable is set with default message, no logger provided
    monkeypatch.setenv('TEST_ENV_VAR', 'test_value')
    result = sample_function()
    captured = capsys.readouterr()
    assert result == "Function executed with env_var_value: test_value"
    assert "Using environment variable TEST_ENV_VAR with value: test_value" in captured.out

def test_env_var_set_logger(monkeypatch, caplog):
    """
    Test case 2: Environment variable is set with custom message, logger provided
    """
    # Test case 2: Environment variable is set with custom message, logger provided
    monkeypatch.setenv('TEST_ENV_VAR', 'test_value')
    with caplog.at_level(logging.INFO):
        result = sample_function_logger()
    assert result == "Function executed with env_var_value: test_value"
    assert "Custom log message" in caplog.text

def test_env_var_not_set(monkeypatch, capsys):
    """
    Test case 3: Environment variable is not set with default message, no logger provided
    """
    # Test case 3: Environment variable is not set with default message, no logger provided
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    result = sample_function()
    captured = capsys.readouterr()
    assert result == "Function executed with env_var_value: None"
    assert "Using default value for TEST_ENV_VAR: None" in captured.out

def test_env_var_not_set_logger(monkeypatch, caplog):
    """
    Test case 4: Environment variable is not set with custom message, logger provided
    """
    # Test case 4: Environment variable is not set with custom message, logger provided
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    with caplog.at_level(logging.INFO):
        result = sample_function_logger()
    assert result == "Function executed with env_var_value: default_value"
    assert "Custom log message" in caplog.text

def test_env_var_required_not_set(monkeypatch):
    """
    Test case 5: Required environment variable is not set, no logger provided
    """
    # Test case 5: Required environment variable is not set, no logger provided
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    with pytest.raises(ValueError, match="Required environment variable TEST_ENV_VAR is not set"):
        @env_config('TEST_ENV_VAR', required=True)
        def sample_function_required(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_env_var_required_not_set_logger(monkeypatch, caplog):
    """
    Test case 6: Required environment variable is not set, logger provided
    """
    # Test case 6: Required environment variable is not set, logger provided
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    with caplog.at_level(logging.ERROR):
        @env_config('TEST_ENV_VAR', logger=test_logger, required=True)
        def sample_function_required(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        result = sample_function_required()
    assert result is None
    assert "Required environment variable TEST_ENV_VAR is not set" in caplog.text

def test_env_var_type_conversion(monkeypatch, capsys):
    """
    Test case 7: Environment variable type conversion, no logger provided
    """
    # Test case 7: Environment variable type conversion, no logger provided
    monkeypatch.setenv('TEST_ENV_VAR', '123')
    @env_config('TEST_ENV_VAR', var_type=int)
    def sample_function_type(env_var_value=None):
        return f"Function executed with env_var_value: {env_var_value}"
    result = sample_function_type()
    captured = capsys.readouterr()
    assert result == "Function executed with env_var_value: 123"
    assert "Using environment variable TEST_ENV_VAR with value: 123" in captured.out

def test_env_var_type_conversion_logger(monkeypatch, caplog):
    """
    Test case 8: Environment variable type conversion, logger provided
    """
    # Test case 8: Environment variable type conversion, logger provided
    monkeypatch.setenv('TEST_ENV_VAR', '123')
    @env_config('TEST_ENV_VAR', logger=test_logger, var_type=int)
    def sample_function_type(env_var_value=None):
        return f"Function executed with env_var_value: {env_var_value}"
    with caplog.at_level(logging.INFO):
        result = sample_function_type()
    assert result == "Function executed with env_var_value: 123"
    assert "Using environment variable TEST_ENV_VAR with value: 123" in caplog.text

def test_env_var_invalid_type_conversion(monkeypatch):
    """
    Test case 9: Environment variable type conversion, no logger provided
    """
    # Test case 9: Environment variable type conversion, no logger provided
    monkeypatch.setenv('TEST_ENV_VAR', 'invalid_int')
    with pytest.raises(ValueError, match="Environment variable TEST_ENV_VAR cannot be converted to int"):
        @env_config('TEST_ENV_VAR', var_type=int)
        def sample_function_type(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_env_var_invalid_type_conversion_logger(monkeypatch, caplog):
    """
    Test case 10: Invalid environment variable type conversion, logger provided
    """
    # Test case 10: Invalid environment variable type conversion, logger provided
    monkeypatch.setenv('TEST_ENV_VAR', 'invalid_int')
    with caplog.at_level(logging.ERROR):
        @env_config('TEST_ENV_VAR', logger=test_logger, var_type=int)
        def sample_function_invalid_type(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        result = sample_function_invalid_type()
    assert result is None
    assert "Environment variable TEST_ENV_VAR cannot be converted to int" in caplog.text

def test_invalid_logger():
    """
    Test case 10: Invalid logger (not an instance of logging.Logger or None)
    """
    # Test case 10: Invalid logger (not an instance of logging.Logger or None)
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @env_config('TEST_ENV_VAR', logger="not_a_logger")
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_invalid_var_name():
    """
    Test case 11: Invalid var_name (not a non-empty string), no logger provided
    """
    # Test case 11: Invalid var_name (not a non-empty string), no logger provided
    with pytest.raises(TypeError, match="var_name must be a non-empty string"):
        @env_config(123)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_invalid_required():
    """
    Test case 12: Invalid required (not a boolean), no logger provided
    """
    # Test case 12: Invalid required (not a boolean), no logger provided
    with pytest.raises(TypeError, match="required must be a boolean"):
        @env_config('TEST_ENV_VAR', required="not_a_boolean")
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_invalid_var_type():
    """
    Test case 13: Invalid var_type (not a type), no logger provided
    """
    # Test case 13: Invalid var_type (not a type), no logger provided
    with pytest.raises(TypeError, match="var_type must be a type"):
        @env_config('TEST_ENV_VAR', var_type="not_a_type")
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_invalid_custom_message():
    """
    Test case 14: Invalid custom_message (not a string or None), no logger provided
    """
    # Test case 14: Invalid custom_message (not a string or None), no logger provided
    with pytest.raises(TypeError, match="custom_message must be a string or None"):
        @env_config('TEST_ENV_VAR', custom_message=123)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"

def test_invalid_var_name_with_logger(caplog):
    """
    Test case 15: Invalid var_name (not a non-empty string), logger provided
    """
    # Test case 15: Invalid var_name (not a non-empty string), logger provided
    with caplog.at_level(logging.ERROR):
        @env_config(123, logger=test_logger)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        with pytest.raises(TypeError):
            sample_function()
    assert "var_name must be a non-empty string" in caplog.text

def test_invalid_required_with_logger(caplog):
    """
    Test case 16: Invalid required (not a boolean), logger provided
    """
    # Test case 16: Invalid required (not a boolean), logger provided
    with caplog.at_level(logging.ERROR):
        @env_config('TEST_ENV_VAR', required="not_a_boolean", logger=test_logger)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        with pytest.raises(TypeError):
            sample_function()
    assert "required must be a boolean" in caplog.text

def test_invalid_var_type_with_logger(caplog):
    """
    Test case 17: Invalid var_type (not a type), logger provided
    """
    # Test case 17: Invalid var_type (not a type), logger provided
    with caplog.at_level(logging.ERROR):
        @env_config('TEST_ENV_VAR', var_type="not_a_type", logger=test_logger)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        with pytest.raises(TypeError):
            sample_function()
    assert "var_type must be a type" in caplog.text

def test_invalid_custom_message_with_logger(caplog):
    """
    Test case 18: Invalid custom_message (not a string or None), logger provided
    """
    # Test case 18: Invalid custom_message (not a string or None), logger provided
    with caplog.at_level(logging.ERROR):
        @env_config('TEST_ENV_VAR', custom_message=123, logger=test_logger)
        def sample_function(env_var_value=None):
            return f"Function executed with env_var_value: {env_var_value}"
        with pytest.raises(TypeError):
            sample_function()
    assert "custom_message must be a string or None" in caplog.text
