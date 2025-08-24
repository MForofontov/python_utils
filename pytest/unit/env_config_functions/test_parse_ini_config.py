import pytest
import tempfile
import os
import configparser
from env_config_functions.parse_ini_config import parse_ini_config

def write_ini_file(data, path):
    parser = configparser.ConfigParser()
    for section, values in data.items():
        parser[section] = values
    with open(path, 'w') as f:
        parser.write(f)

def test_parse_ini_config_basic():
    """
    Test case 1: Basic INI config loads as dict
    """
    data = {'section1': {'a': '1'}, 'section2': {'b': '2'}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ini') as tf:
        write_ini_file(data, tf.name)
        tf.close()
        config = parse_ini_config(tf.name)
        assert config == data
    os.remove(tf.name)

def test_parse_ini_config_required_sections():
    """
    Test case 2: Missing required sections raises ValueError
    """
    data = {'section1': {'a': '1'}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ini') as tf:
        write_ini_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='Missing required config sections'):
            parse_ini_config(tf.name, required_sections=['section1', 'section2'])
    os.remove(tf.name)

def test_parse_ini_config_schema_validator():
    """
    Test case 3: Custom schema validator raises ValueError
    """
    data = {'section1': {'a': '1'}}
    def schema(cfg):
        if 'section2' not in cfg:
            raise ValueError('section2 required')
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ini') as tf:
        write_ini_file(data, tf.name)
        tf.close()
        with pytest.raises(ValueError, match='section2 required'):
            parse_ini_config(tf.name, schema_validator=schema)
    os.remove(tf.name)
