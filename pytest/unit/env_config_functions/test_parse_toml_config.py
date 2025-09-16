import toml

import pytest
from env_config_functions.parse_toml_config import parse_toml_config


def write_toml_file(data, path):
    with open(path, "w") as f:
        toml.dump(data, f)


def test_parse_toml_config_basic(tmp_path):
    """
    Test case 1: Basic TOML config loads as dict
    """
    data = {"a": 1, "b": {"c": 2}}
    config_file = tmp_path / "config.toml"
    write_toml_file(data, config_file)
    config = parse_toml_config(str(config_file))
    assert config == data


def test_parse_toml_config_required_keys(tmp_path):
    """
    Test case 2: Missing required keys raises ValueError
    """
    data = {"a": 1}
    config_file = tmp_path / "config.toml"
    write_toml_file(data, config_file)
    with pytest.raises(ValueError, match="Missing required config keys"):
        parse_toml_config(str(config_file), required_keys=["a", "b"])


def test_parse_toml_config_schema_validator(tmp_path):
    """
    Test case 3: Custom schema validator raises ValueError
    """
    data = {"a": 1}

    def schema(cfg):
        if "b" not in cfg:
            raise ValueError("b required")

    config_file = tmp_path / "config.toml"
    write_toml_file(data, config_file)
    with pytest.raises(ValueError, match="b required"):
        parse_toml_config(str(config_file), schema_validator=schema)


def test_parse_toml_config_invalid_toml(tmp_path):
    """
    Test case 4: Invalid TOML raises toml.TomlDecodeError
    """
    config_file = tmp_path / "config.toml"
    config_file.write_text('a = 1\nb = "unterminated')  # malformed TOML
    with pytest.raises(toml.TomlDecodeError):
        parse_toml_config(str(config_file))


def test_parse_toml_config_not_dict(tmp_path, monkeypatch):
    """
    Test case 5: TOML that is not a dict raises ValueError
    """
    config_file = tmp_path / "config.toml"
    config_file.write_text("a = 1")

    def fake_load(f):
        return [1, 2, 3]

    monkeypatch.setattr(toml, "load", fake_load)
    with pytest.raises(ValueError, match="must be a dictionary"):
        parse_toml_config(str(config_file))
