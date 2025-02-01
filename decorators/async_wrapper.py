import asyncio
import inspect
import logging
from functools import wraps
from typing import Any, Callable, Optional

def async_wrapper(logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Wraps a synchronous function to be executed asynchronously.

    Parameters
    ----------
    logger : Optional[logging.Logger]
        The logger to use for logging errors. If None, the default logger will be used.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A decorator that wraps a synchronous function in an async wrapper.
    
    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    if logger and not isinstance(logger, logging.Logger):
        raise TypeError("The logger must be an instance of logging.Logger")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The synchronous function to be wrapped.
        
        Returns
        -------
        Callable[..., Any]
            The wrapped function with asynchronous execution.

        Raises
        ------
        TypeError
            If the function is asynchronous.
        """
        if inspect.iscoroutinefunction(func):
            error_message = "The function to be wrapped must be synchronous"
            if logger:
                logger.error(f"An error occurred in {func.__name__}: {error_message}", exc_info=True)
            raise TypeError(error_message)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Asynchronous wrapper function.

            Parameters
            ----------
            *args : Any
                Positional arguments to pass to the wrapped function.
            **kwargs : Any
                Keyword arguments to pass to the wrapped function.

            Returns
            -------
            Any
                The result of the wrapped function.
            """
            try:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, func, *args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"An error occurred in {func.__name__}: {e}", exc_info=True)
                raise

        return wrapper
    
    return decorator  # Return the decorator instead of the wrapper itself
