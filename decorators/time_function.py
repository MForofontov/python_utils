import time
import logging
from typing import Any
from collections.abc import Callable
from functools import wraps
from logger_functions.logger import validate_logger

def time_function(logger: logging.Logger | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator that measures and logs or prints the execution time of a function.

    Parameters
    ----------
    logger : Optional[logging.Logger]
        The logger to use for logging the execution time. If None, the execution time is printed to the console.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The wrapped function that measures and logs or prints its execution time.
    
    Raises
    ------
    TypeError
        If logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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
