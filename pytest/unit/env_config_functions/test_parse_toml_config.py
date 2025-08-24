import pytest
import tempfile
import os
import toml
from env_config_functions.parse_toml_config import parse_toml_config

def write_toml_file(data, path):
    with open(path, 'w') as f:
        toml.dump(data, f)

def test_parse_toml_config_basic():
    """
    Test case 1: Basic TOML config loads as dict
    """
    data = {'a': 1, 'b': {'c': 2}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.toml') as tf:
        write_toml_file(data, tf.name)
        tf.close()
        config = parse_toml_config(tf.name)
        assert config == data
    os.remove(tf.name)

def test_parse_toml_config_required_keys():
    """
    Test case 2: Missing required keys raises ValueError
    """
    data = {'a': 1}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.toml') as tf:
        write_toml_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='Missing required config keys'):
            parse_toml_config(tf.name, required_keys=['a', 'b'])
    os.remove(tf.name)

def test_parse_toml_config_schema_validator():
    """
    Test case 3: Custom schema validator raises ValueError
    """
    data = {'a': 1}
    def schema(cfg):
        if 'b' not in cfg:
            raise ValueError('b required')
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.toml') as tf:
        write_toml_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='b required'):
            parse_toml_config(tf.name, schema_validator=schema)
    os.remove(tf.name)

def test_parse_toml_config_invalid_toml():
    """
    Test case 4: Invalid TOML raises toml.TomlDecodeError
    """
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.toml') as tf:
        tf.write('a = 1\nb = [1, 2\n')  # malformed TOML
        tf.close()
        with pytest.raises(toml.TomlDecodeError):
            parse_toml_config(tf.name)
    os.remove(tf.name)

def test_parse_toml_config_not_dict():
    """
    Test case 5: TOML that is not a dict raises ValueError
    """
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.toml') as tf:
        tf.write('[[array]]\nvalue = 1\n')
        tf.close()
        with pytest.raises(ValueError, match='must be a dictionary'):
            parse_toml_config(tf.name)
    os.remove(tf.name)
