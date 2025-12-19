"""
Module for getting environment variables.
"""

import os


def get_environment_variable(
    var_name: str,
    default: str | None = None,
    required: bool = False,
) -> str | None:
    """
    Get an environment variable with optional default and validation.

    Parameters
    ----------
    var_name : str
        Name of the environment variable.
    default : str | None, optional
        Default value if variable is not set (by default None).
    required : bool, optional
        Whether the variable is required (by default False).

    Returns
    -------
    str | None
        Value of the environment variable or default value.

    Raises
    ------
    TypeError
        If var_name is not a string.
    ValueError
        If required=True and variable is not set.

    Examples
    --------
    >>> import os
    >>> os.environ['TEST_VAR'] = 'test_value'
    >>> get_environment_variable('TEST_VAR')
    'test_value'
    >>> get_environment_variable('NONEXISTENT', default='default')
    'default'
    >>> del os.environ['TEST_VAR']

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(var_name, str):
        raise TypeError(f"var_name must be a string, got {type(var_name).__name__}")
    
    if not isinstance(required, bool):
        raise TypeError(f"required must be a boolean, got {type(required).__name__}")
    
    if default is not None and not isinstance(default, str):
        raise TypeError(f"default must be a string or None, got {type(default).__name__}")

    value = os.environ.get(var_name, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{var_name}' is not set")
    
    return value


__all__ = ['get_environment_variable']
