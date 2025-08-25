import os
from env_config_functions.load_dotenv import load_dotenv


def test_load_dotenv_basic(tmp_path):
    """
    Test case 1: Basic .env file loading.
    """
    config_file = tmp_path / "config.env"
    config_file.write_text('FOO=bar\nBAZ=qux\n')
    # Clear env vars first
    os.environ.pop('FOO', None)
    os.environ.pop('BAZ', None)
    load_dotenv(str(config_file))
    assert os.environ['FOO'] == 'bar'
    assert os.environ['BAZ'] == 'qux'


def test_load_dotenv_override(tmp_path):
    """
    Test case 2: Override existing environment variables.
    """
    os.environ['EXISTING'] = 'old'
    config_file = tmp_path / "config.env"
    config_file.write_text('EXISTING=new\n')
    load_dotenv(str(config_file), override=True)
    assert os.environ['EXISTING'] == 'new'


def test_load_dotenv_no_override(tmp_path):
    """
    Test case 3: Don't override existing environment variables.
    """
    os.environ['EXISTING'] = 'old'
    config_file = tmp_path / "config.env"
    config_file.write_text('EXISTING=new\n')
    load_dotenv(str(config_file), override=False)
    assert os.environ['EXISTING'] == 'old'


def test_load_dotenv_comments(tmp_path):
    """
    Test case 4: Skip comments and empty lines.
    """
    config_file = tmp_path / "config.env"
    config_file.write_text('# This is a comment\nVAR1=value1\n\n# Another comment\nVAR2=value2\n')
    os.environ.pop('VAR1', None)
    os.environ.pop('VAR2', None)
    load_dotenv(str(config_file))
    assert os.environ['VAR1'] == 'value1'
    assert os.environ['VAR2'] == 'value2'


def test_load_dotenv_nonexistent_file():
    """
    Test case 5: Nonexistent file doesn't raise error.
    """
    load_dotenv('nonexistent.env')  # Should not raise
