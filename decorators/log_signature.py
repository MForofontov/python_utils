from typing import Callable, Any, Optional
from functools import wraps
import inspect
import logging

def log_signature(logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to log the function signature and the arguments passed to it.

    Parameters
    ----------
    logger : Optional[logging.Logger]
        The logger to use for logging. If None, a default logger is used.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    if isinstance(logger, logging.Logger):
        raise TypeError("logger must be an instance of logging.Logger.")

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
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that logs the function signature and arguments.

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
            signature = inspect.signature(func)
            logger.info(f"Executing {func.__name__}{signature} with args: {args} and kwargs: {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return decorator