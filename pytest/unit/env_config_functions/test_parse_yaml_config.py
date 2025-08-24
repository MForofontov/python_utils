import pytest
import tempfile
import os
import yaml
from env_config_functions.parse_yaml_config import parse_yaml_config

def write_yaml_file(data, path):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)

def test_parse_yaml_config_basic():
    """
    Test case 1: Basic YAML config loads as dict
    """
    data = {'a': 1, 'b': {'c': 2}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.yaml') as tf:
        write_yaml_file(data, tf.name)
        tf.close()
        config = parse_yaml_config(tf.name)
        assert config == data
    os.remove(tf.name)

def test_parse_yaml_config_required_keys():
    """
    Test case 2: Missing required keys raises ValueError
    """
    data = {'a': 1}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.yaml') as tf:
        write_yaml_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='Missing required config keys'):
            parse_yaml_config(tf.name, required_keys=['a', 'b'])
    os.remove(tf.name)

def test_parse_yaml_config_schema_validator():
    """
    Test case 3: Custom schema validator raises ValueError
    """
    data = {'a': 1}
    def schema(cfg):
        if 'b' not in cfg:
            raise ValueError('b required')
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.yaml') as tf:
        write_yaml_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='b required'):
            parse_yaml_config(tf.name, schema_validator=schema)
    os.remove(tf.name)

def test_parse_yaml_config_invalid_yaml():
    """
    Test case 4: Invalid YAML raises yaml.YAMLError
    """
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.yaml') as tf:
        tf.write('a: 1\nb: [1, 2\n')  # malformed YAML
        tf.close()
        with pytest.raises(yaml.YAMLError):
            parse_yaml_config(tf.name)
    os.remove(tf.name)

def test_parse_yaml_config_not_dict():
    """
    Test case 5: YAML that is not a dict raises ValueError
    """
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.yaml') as tf:
        write_yaml_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='must be a dictionary'):
            parse_yaml_config(tf.name)
    os.remove(tf.name)
