from typing import Callable, Any, Optional
from functools import wraps
import logging

def handle_error(error_message: str, logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to handle exceptions in the decorated function. If an exception occurs,
    it logs a specified error message and returns None.

    Parameters
    ----------
    error_message : str
        The error message to log if an exception occurs.
    logger : Optional[logging.Logger]
        The logger to use for logging. If None, logging is disabled.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")

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
            The wrapper function that handles exceptions.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The result of the decorated function, or None if an exception occurs.
            """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"{error_message}: {e}")
                else:
                    print(f"{error_message}: {e}")
                return None
        return wrapper
    return decorator