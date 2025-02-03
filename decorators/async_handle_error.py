from typing import Callable, Any, Optional
from functools import wraps
import asyncio
import inspect
import logging

def async_handle_error(logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to handle errors in asynchronous functions.

    Parameters
    ----------
    error_message : str
        The error message to print when an exception occurs.
    logger : Optional[logging.Logger]
        The logger to use for logging errors. If None, the default logger will be used.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A decorator that wraps the input function with error handling.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("The logger must be an instance of logging.Logger")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The asynchronous function to be wrapped.

        Returns
        -------
        Callable[..., Any]
            The wrapped function with error handling.

        Raises
        ------
        TypeError
            If the function is not asynchronous.
        """
        if not inspect.iscoroutinefunction(func):
            error_message = "The function to be wrapped must be asynchronous"
            if logger:
                logger.error(f"An error occurred in {func.__name__}: {error_message}", exc_info=True)
            else:
                raise TypeError(error_message)
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function to handle errors in the asynchronous function.

            Parameters
            ----------
            *args : Any
                Positional arguments to pass to the wrapped function.
            **kwargs : Any
                Keyword arguments to pass to the wrapped function.

            Returns
            -------
            Any
                The result of the wrapped function, or None if an exception occurs.
            """
            try:
                # Attempt to call the original asynchronous function
                return await func(*args, **kwargs)
            except Exception as e:
                # Print the custom error message and the exception
                print(f"An error occurred in {func.__name__}: {e}")
                # Log the error message and the exception if logging is enabled
                if logger:
                    logger.error(f"An error occurred in {func.__name__}: {e}", exc_info=True)
                # Return None if an exception occurs
                return None
        return wrapper
    return decorator
