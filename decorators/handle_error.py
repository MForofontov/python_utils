from typing import Any, ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import logging
from logger_functions.logger import validate_logger
P = ParamSpec("P")
R = TypeVar("R")


def handle_error(
    error_message: str, logger: logging.Logger | None = None
) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """
    A decorator to handle exceptions in the decorated function. If an exception occurs,
    it logs a specified error message and returns None.

    Parameters
    ----------
    error_message : str
        The error message to log if an exception occurs.
    logger : Optional[logging.Logger]
        The logger to use for logging. If None, logging is disabled.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R | None]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)

    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be decorated.

        Returns
        -------
        Callable[P, R | None]
            The wrapped function.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            """
            The wrapper function that handles exceptions.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The result of the decorated function, or None if an exception occurs.
            """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"{error_message}: {e}")
                else:
                    print(f"{error_message}: {e}")
                return None

        return wrapper

    return decorator

__all__ = ['handle_error']