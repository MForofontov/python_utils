"""
Module for setting environment variables.
"""

import os


def set_environment_variable(var_name: str, value: str) -> None:
    """
    Set an environment variable.

    Parameters
    ----------
    var_name : str
        Name of the environment variable.
    value : str
        Value to set for the environment variable.

    Raises
    ------
    TypeError
        If var_name or value is not a string.
    ValueError
        If var_name is empty.

    Examples
    --------
    >>> set_environment_variable('MY_VAR', 'my_value')
    >>> import os
    >>> os.environ.get('MY_VAR')
    'my_value'

    Notes
    -----
    This only sets the variable for the current process and its children.
    The variable will not persist after the process terminates.

    Complexity
    ----------
    Time: O(1), Space: O(n) where n is length of value
    """
    if not isinstance(var_name, str):
        raise TypeError(f"var_name must be a string, got {type(var_name).__name__}")
    
    if not isinstance(value, str):
        raise TypeError(f"value must be a string, got {type(value).__name__}")
    
    if not var_name:
        raise ValueError("var_name cannot be empty")
    
    os.environ[var_name] = value


__all__ = ['set_environment_variable']
