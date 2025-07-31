from typing import Any
from collections.abc import Callable
from collections import deque
from functools import wraps
import time
import logging
from logger_functions.logger import validate_logger


class RateLimitExceededException(Exception):
    """Exception raised when the rate limit is exceeded."""


def rate_limit(
    max_calls: int,
    period: int,
    logger: logging.Logger | None = None,
    exception_message: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to limit the number of times a function can be called within a specific period.

    Parameters
    ----------
    max_calls : int
        The maximum number of allowed calls within the period.
    period : int
        The time period in seconds.
    logger : Optional[logging.Logger]
        The logger to use for logging rate limit warnings.
    exception_message : Optional[str]
        Custom exception message when the rate limit is exceeded.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    ValueError
        If either max_calls or period is not a positive integer.
    TypeError
        If logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)
    if not isinstance(max_calls, int) or max_calls <= 0:
        if logger:
            logger.error("max_calls must be a positive integer", exc_info=True)
        raise ValueError("max_calls must be a positive integer")
    if not isinstance(period, int) or period <= 0:
        if logger:
            logger.error("period must be a positive integer", exc_info=True)
        raise ValueError("period must be a positive integer")
    if not isinstance(exception_message, str) and exception_message is not None:
        if logger:
            logger.error("exception_message must be a string or None", exc_info=True)
        raise TypeError("exception_message must be a string or None")

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
            The wrapped function
        """
        # Store timestamps of function calls using a deque with fixed length
        calls: deque[float] = deque(maxlen=max_calls)

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

            Raises
            ------
            RateLimitExceededException
                If the rate limit is exceeded.
            """
            nonlocal calls  # Indicates that 'calls' refers to the deque in the enclosing scope
            current_time = time.time()
            # Remove calls that are outside the allowed period
            while calls and current_time - calls[0] >= period:
                calls.popleft()

            # Check if the number of calls exceeds the limit
            if len(calls) >= max_calls:
                message = (
                    exception_message
                    or f"Rate limit exceeded for {func.__name__}. Try again later."
                )
                if logger:
                    logger.warning(message, exc_info=True)
                raise RateLimitExceededException(message)

            # Append the current timestamp to the list of calls
            calls.append(current_time)
            return func(*args, **kwargs)

        return wrapper

    return decorator

__all__ = ['RateLimitExceededException', 'rate_limit']
