from typing import Any
from collections.abc import Callable
from functools import wraps
import time
import logging

def throttle(rate_limit: int | float, logger: logging.Logger = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to enforce a rate limit on a function, ensuring it is not called more often than the specified rate.

    Parameters
    ----------
    rate_limit : float
        The minimum time interval (in seconds) between consecutive calls to the function.
    logger : logging.Logger, optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If rate_limit is not a float or an integer.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")

    if not isinstance(rate_limit, (int, float)) or rate_limit < 0:
        if logger:
            logger.error("Type error in throttle decorator: rate_limit must be a positive float or an integer.", exc_info=True)
        raise TypeError("rate_limit must be a positive float or an integer")

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
        last_called = 0.0

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that enforces the rate limit.

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
            nonlocal last_called
            current_time = time.time()
            elapsed_time = current_time - last_called
            if elapsed_time < rate_limit:
                if logger:
                    logger.error(f"Function {func.__name__} called too frequently. Rate limit: {rate_limit} seconds.", exc_info=True)
                raise RuntimeError(f"Function {func.__name__} called too frequently. Rate limit: {rate_limit} seconds.")
            last_called = current_time
            return func(*args, **kwargs)
        return wrapper
    return decorator