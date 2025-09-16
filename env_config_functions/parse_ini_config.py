import configparser
from collections.abc import Callable
from typing import Any


def parse_ini_config(
    path: str,
    schema_validator: Callable[[dict[str, Any]], None] | None = None,
    required_sections: list[str] | None = None,
) -> dict[str, Any]:
    """
    Parse an INI configuration file and return a dictionary, with optional schema validation.

    Parameters
    ----------
    path : str
        Path to the INI file.
    schema_validator : callable, optional
        Function to validate the loaded config dict.
    required_sections : list of str, optional
        List of required section names.

    Returns
    -------
    dict
        Dictionary with config values.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    configparser.Error
        If the INI is invalid.
    ValueError
        If required sections are missing or schema validation fails.

    Examples
    --------
    >>> config = parse_ini_config('config.ini')
    >>> config['database']['host']
    'localhost'
    >>> def schema(cfg):
    ...     if 'database' not in cfg:
    ...         raise ValueError('Missing database section')
    >>> parse_ini_config('config.ini', schema_validator=schema)
    """
    parser = configparser.ConfigParser()
    parser.read(path)
    config = {section: dict(parser.items(section)) for section in parser.sections()}
    if required_sections:
        missing = [s for s in required_sections if s not in config]
        if missing:
            raise ValueError(f"Missing required config sections: {missing}")
    if schema_validator:
        schema_validator(config)
    return config
