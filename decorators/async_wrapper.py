from typing import Callable, Any, Optional
from functools import wraps
import asyncio
import logging
import inspect

def async_wrapper(func: Callable[..., Any], logger: Optional[logging.Logger] = None) -> Callable[..., Any]:
    """
    Wraps a synchronous function to be executed asynchronously.

    Parameters
    ----------
    func : Callable[..., Any]
        The synchronous function to be wrapped.
    logger : Optional[logging.Logger]
        The logger to use for logging errors. If None, the default logger will be used.

    Returns
    -------
    Callable[..., Any]
        An asynchronous wrapper function that executes the input function in an executor.

    Raises
    ------
    TypeError
        If the function is not synchronous.
    """
    if inspect.iscoroutinefunction(func):
        error_message = "The function to be wrapped must be synchronous"
        if logger:
            logger.error(f"An error occurred in {func.__name__}: {error_message}", exc_info=True)
        else:
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
            # Get the current event loop
            loop = asyncio.get_event_loop()
            # Run the synchronous function in an executor and return the result
            return await loop.run_in_executor(None, func, *args, **kwargs)
        except Exception as e:
            if logger:
                logger.error(f"An error occurred in {func.__name__}: {e}", exc_info=True)
            else:
                raise

    return wrapper
