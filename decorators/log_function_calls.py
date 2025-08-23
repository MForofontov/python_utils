import logging
from functools import wraps
from typing import Any, ParamSpec, TypeVar
from collections.abc import Callable
from logger_functions.logger import validate_logger
P = ParamSpec("P")
R = TypeVar("R")


def log_function_calls(
    logger: logging.Logger | None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to log function calls, including arguments passed and the result returned.

    Parameters
    ----------
    logger : logging.Logger | None
        The logger instance to use for logging. Must not be None.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        A decorator that logs the function calls.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or is None.
    """
    validate_logger(logger, allow_none=False)
    assert logger is not None

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            The wrapper function that logs function calls.

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

            Raises
            ------
            Exception
                If an exception occurs during the function call.
            """
            try:
                logger.info(
                    f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}"
                )
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                raise

        return wrapper

    return decorator

__all__ = ['log_function_calls']