import pytest
import tempfile
import os
from env_config_functions.load_dotenv import load_dotenv


def test_load_dotenv_basic():
    """
    Test case 1: Basic .env file loading
    """
    # Test case 1: Basic .env file loading
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('FOO=bar\nBAZ=qux\n')
        tf.close()
        # Clear env vars first
        os.environ.pop('FOO', None)
        os.environ.pop('BAZ', None)
        load_dotenv(tf.name)
        assert os.environ['FOO'] == 'bar'
        assert os.environ['BAZ'] == 'qux'
    os.remove(tf.name)


def test_load_dotenv_override():
    """
    Test case 2: Override existing environment variables
    """
    # Test case 2: Override existing environment variables
    os.environ['EXISTING'] = 'old'
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('EXISTING=new\n')
        tf.close()
        load_dotenv(tf.name, override=True)
        assert os.environ['EXISTING'] == 'new'
    os.remove(tf.name)


def test_load_dotenv_no_override():
    """
    Test case 3: Don't override existing environment variables
    """
    # Test case 3: Don't override existing environment variables
    os.environ['EXISTING'] = 'old'
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('EXISTING=new\n')
        tf.close()
        load_dotenv(tf.name, override=False)
        assert os.environ['EXISTING'] == 'old'
    os.remove(tf.name)


def test_load_dotenv_comments():
    """
    Test case 4: Skip comments and empty lines
    """
    # Test case 4: Skip comments and empty lines
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('# This is a comment\nVAR1=value1\n\n# Another comment\nVAR2=value2\n')
        tf.close()
        os.environ.pop('VAR1', None)
        os.environ.pop('VAR2', None)
        load_dotenv(tf.name)
        assert os.environ['VAR1'] == 'value1'
        assert os.environ['VAR2'] == 'value2'
    os.remove(tf.name)


def test_load_dotenv_nonexistent_file():
    """
    Test case 5: Nonexistent file doesn't raise error
    """
    # Test case 5: Nonexistent file doesn't raise error
    load_dotenv('nonexistent.env')  # Should not raise
