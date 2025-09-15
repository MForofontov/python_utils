from typing import Any
from collections.abc import Callable
import yaml


def parse_yaml_config(
    path: str,
    schema_validator: Callable[[dict[str, Any]], None] | None = None,
    required_keys: list[str] | None = None,
) -> dict[str, Any]:
    """
    Parse a YAML configuration file and return a dictionary, with optional schema validation.

    Parameters
    ----------
    path : str
        Path to the YAML file.
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
    yaml.YAMLError
        If the YAML is invalid.
    ValueError
        If required keys are missing or schema validation fails.

    Examples
    --------
    >>> config = parse_yaml_config('config.yaml')
    >>> config['database']['host']
    'localhost'
    >>> def schema(cfg):
    ...     if 'database' not in cfg:
    ...         raise ValueError('Missing database section')
    >>> parse_yaml_config('config.yaml', schema_validator=schema)
    """
    with open(path) as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        raise ValueError("YAML config must be a dictionary at the top level")
    if required_keys:
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
    if schema_validator:
        schema_validator(config)
    return config
