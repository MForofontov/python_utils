from typing import Any
from collections.abc import Callable
from functools import wraps
import logging

def manipulate_output(manipulation_func: Callable[[Any], Any], logger: logging.Logger | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to manipulate the output of a function using a specified manipulation function.

    Parameters
    ----------
    manipulation_func : Callable[[Any], Any]
        The function to manipulate the output of the decorated function.
    logger : Optional[logging.Logger]
        The logger to use for logging manipulation warnings.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
        If the manipulation_func is not a callable function.
    """
    if logger is not None and not isinstance(logger, logging.Logger):
        raise TypeError("logger must be an instance of logging.Logger or None.")
    if not callable(manipulation_func):
        if logger is not None:
            logger.error("manipulation_func must be a callable function.")
        raise TypeError("manipulation_func must be a callable function.")

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
            The wrapper function that manipulates the output.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The manipulated result of the decorated function.
            """
            result = func(*args, **kwargs)
            manipulated_result = manipulation_func(result)
            return manipulated_result

        return wrapper
    return decorator
