from typing import Any
from collections.abc import Callable
from functools import wraps
import os
import logging
from logger_functions.logger import validate_logger


def env_config(
    var_name: str,
    required: bool = True,
    var_type: type = str,
    custom_message: str | None = None,
    logger: logging.Logger | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to inject environment variables into a function.

    Parameters
    ----------
    var_name : str
        The name of the environment variable.
    required : bool, optional
        Whether the environment variable is required (default is True).
    var_type : Type, optional
        The expected type of the environment variable (default is str).
    custom_message : Optional[str], optional
        Custom error message if the environment variable is missing or invalid (default is None).
    logger : Optional[logging.Logger], optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If any of the parameters do not match the expected types.
    """

    def log_or_raise_error(message: str) -> None:
        """
        Helper function to log an error or raise an exception.

        Parameters
        ----------
        message : str
            The error message to log or raise.
        """
        if logger:
            logger.error(message, exc_info=True)
        raise TypeError(message)

    validate_logger(logger)

    if not isinstance(var_name, str) or not var_name:
        log_or_raise_error("var_name must be a non-empty string")

    if not isinstance(required, bool):
        log_or_raise_error("required must be a boolean")

    if not isinstance(var_type, type):
        log_or_raise_error("var_type must be a type")

    if not isinstance(custom_message, str) and custom_message is not None:
        log_or_raise_error("custom_message must be a string or None")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to be decorated.

        Returns
        -------
        Callable[..., Any]
            The wrapped function.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that injects the environment variable.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The result of the decorated function.
            """
            env_value = os.getenv(var_name)
            if env_value is None:
                if required:
                    message = (
                        custom_message
                        or f"Environment variable '{var_name}' is required but not set."
                    )
                    log_or_raise_error(message)
                else:
                    env_value = None
            else:
                try:
                    env_value = var_type(env_value)
                except ValueError:
                    message = (
                        custom_message
                        or f"Environment variable '{var_name}' must be of type {var_type.__name__}."
                    )
                    log_or_raise_error(message)

            kwargs[var_name.lower()] = env_value
            return func(*args, **kwargs)

        return wrapper

    return decorator

__all__ = ['env_config']
