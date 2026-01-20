"""TOML configuration file parsing."""

from collections.abc import Callable
from typing import Any

import toml


def parse_toml_config(
    path: str,
    schema_validator: Callable[[dict[str, Any]], None] | None = None,
    required_keys: list[str] | None = None,
) -> dict[str, Any]:
    """
    Parse a TOML configuration file and return a dictionary, with optional schema validation.

    Parameters
    ----------
    path : str
        Path to the TOML file.
    schema_validator : callable, optional
        Function to validate the loaded config dict.
    required_keys : list of str, optional
        List of required top-level keys.

    Returns
    -------
    dict
        Dictionary with config values.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    toml.TomlDecodeError
        If the TOML is invalid.
    ValueError
        If required keys are missing or schema validation fails.

    Examples
    --------
    >>> config = parse_toml_config('config.toml')
    >>> config['database']['host']
    'localhost'
    >>> def schema(cfg):
    ...     if 'database' not in cfg:
    ...         raise ValueError('Missing database section')
    >>> parse_toml_config('config.toml', schema_validator=schema)
    """
    with open(path) as f:
        config = toml.load(f)
    if not isinstance(config, dict):
        raise ValueError("TOML config must be a dictionary at the top level")
    if required_keys:
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
    if schema_validator:
        schema_validator(config)
    return config
