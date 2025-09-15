import os
from typing import Any
from collections.abc import Callable


def get_env_var(
    key: str, default: Any | None = None, cast: Callable[[str], Any] | None = None
) -> Any:
    """
    Get an environment variable with optional type casting and default value.

    Parameters
    ----------
    key : str
        The environment variable name.
    default : Any, optional
        Value to return if variable is not set.
    cast : callable, optional
        Function to cast the value (e.g., int, float, bool).

    Returns
    -------
    Any
        The environment variable value, cast if specified, or default if not set.

    Raises
    ------
    ValueError
        If casting fails.

    Examples
    --------
    >>> import os
    >>> os.environ['PORT'] = '8080'
    >>> get_env_var('PORT', cast=int)
    8080
    >>> get_env_var('DEBUG', default=False, cast=lambda v: v.lower() == 'true')
    False
    """
    value = os.environ.get(key, default)
    if value is not None and cast is not None:
        try:
            return cast(value)
        except Exception as e:
            raise ValueError(f"Failed to cast env var {key}: {e}")
    return value
