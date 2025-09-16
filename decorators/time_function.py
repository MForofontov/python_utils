import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def time_function(
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator that measures and logs or prints the execution time of a function.

    Parameters
    ----------
    logger : logging.Logger | None
        The logger to use for logging the execution time. If None, the execution time is printed to the console.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The wrapped function that measures and logs or prints its execution time.

    Raises
    ------
    TypeError
        If logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            The wrapper function that measures the execution time.

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
            # Record the start time
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                message = f"{func.__name__} executed in {execution_time:.4f} seconds"
                if logger:
                    logger.debug(message)
                else:
                    print(message)
            return result

        return wrapper

    return decorator


__all__ = ["time_function"]
