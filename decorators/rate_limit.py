from typing import Callable, Any, Optional, List
import time
import logging

class RateLimitExceededException(Exception):
    """Exception raised when the rate limit is exceeded."""
    pass

def rate_limit(max_calls: int, period: int, logger: Optional[logging.Logger] = None, exception_message: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
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
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")
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
        # List to store the timestamps of function calls
        calls: List[float] = []

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
            nonlocal calls  # Indicates that 'calls' refers to the list in the enclosing scope
            current_time = time.time()
            # Filter out calls that are outside the period
            calls = [call for call in calls if current_time - call < period]
            # Check if the number of calls exceeds the limit
            if len(calls) >= max_calls:
                message = exception_message or f"Rate limit exceeded for {func.__name__}. Try again later."
                if logger:
                    logger.warning(message, exc_info=True)
                raise RateLimitExceededException(message)

            # Append the current timestamp to the list of calls
            calls.append(current_time)
            return func(*args, **kwargs)

        return wrapper
    return decorator
