from typing import Callable, Any, Union
from functools import wraps
import logging
import time

def retry(max_retries: int, delay: Union[int, float] = 1.0, logger: logging.Logger = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to retry a function call a specified number of times with a delay between attempts.

    Parameters
    ----------
    max_retries : int
        The maximum number of retry attempts.
    delay : Union[int, float], optional
        The delay between retry attempts in seconds (default is 1.0).
    logger : logging.Logger, optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If max_retries is not an integer or delay is not a float.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")
    if not isinstance(max_retries, int) or max_retries < 0:
        if logger:
            logger.error("Type error in retry decorator: max_retries must be an integer.", exc_info=True)
        raise TypeError("max_retries must be an positive integer or 0")
    if not isinstance(delay, (int, float)) or delay < 0:
        if logger:
            logger.error("Type error in retry decorator: delay must be a float or an integer.", exc_info=True)
        raise TypeError("delay must be a positive float or an positive integer or 0")

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
            The wrapped function with retry logic.
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that retries the function call.

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
                If the maximum number of retries is exceeded.
            """
            attempts: int = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if logger:
                        logger.error(f"Attempt {attempts} failed for {func.__name__}: {e}", exc_info=True)
                    if attempts >= max_retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
