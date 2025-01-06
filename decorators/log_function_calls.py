import logging
from typing import Callable, Any, Optional

def log_function_calls(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    """
    A decorator to log the function calls, including the arguments passed and the result returned.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to be decorated.

    Returns
    -------
    Callable[..., Any]
        The decorated function with logging.

    Raises
    ------
    None
    """
    if isinstance(logger, logging.Logger):
        raise TypeError("logger must be an instance of logging.Logger.")
    
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper function that logs the function calls.

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
        logger.info(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper
