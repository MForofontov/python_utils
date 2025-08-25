import pytest
import tempfile
import os
from env_config_functions.load_dotenv import load_dotenv


def test_load_dotenv_basic(monkeypatch):
    """
    Test case 1: Basic .env file loading.
    """
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('FOO=bar\nBAZ=qux\n')
        tf.close()
        # Clear env vars first
        monkeypatch.delenv('FOO', raising=False)
        monkeypatch.delenv('BAZ', raising=False)
        load_dotenv(tf.name)
        assert os.environ['FOO'] == 'bar'
        assert os.environ['BAZ'] == 'qux'
    os.remove(tf.name)


def test_load_dotenv_override(monkeypatch):
    """
    Test case 2: Override existing environment variables.
    """
    monkeypatch.setenv('EXISTING', 'old')
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('EXISTING=new\n')
        tf.close()
        load_dotenv(tf.name, override=True)
        assert os.environ['EXISTING'] == 'new'
    os.remove(tf.name)


def test_load_dotenv_no_override(monkeypatch):
    """
    Test case 3: Don't override existing environment variables.
    """
    monkeypatch.setenv('EXISTING', 'old')
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('EXISTING=new\n')
        tf.close()
        load_dotenv(tf.name, override=False)
        assert os.environ['EXISTING'] == 'old'
    os.remove(tf.name)


def test_load_dotenv_comments(monkeypatch):
    """
    Test case 4: Skip comments and empty lines.
    """
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.env') as tf:
        tf.write('# This is a comment\nVAR1=value1\n\n# Another comment\nVAR2=value2\n')
        tf.close()
        monkeypatch.delenv('VAR1', raising=False)
        monkeypatch.delenv('VAR2', raising=False)
        load_dotenv(tf.name)
        assert os.environ['VAR1'] == 'value1'
        assert os.environ['VAR2'] == 'value2'
    os.remove(tf.name)


def test_load_dotenv_nonexistent_file(monkeypatch):
    """
    Test case 5: Nonexistent file doesn't raise error.
    """
    load_dotenv('nonexistent.env')  # Should not raise
