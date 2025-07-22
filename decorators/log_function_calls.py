import logging
from functools import wraps
from typing import Any
from collections.abc import Callable

def log_function_calls(logger: logging.Logger) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to log function calls, including arguments passed and the result returned.

    Parameters
    ----------
    logger : logging.Logger
        The logger instance to use for logging.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A decorator that logs the function calls.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    if not isinstance(logger, logging.Logger):
        raise TypeError("logger must be an instance of logging.Logger.")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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
                logger.info(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                raise Exception(f"Exception in {func.__name__}:") from e

        return wrapper
    
    return decorator
