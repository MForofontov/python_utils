from typing import Any, ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import logging
from logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def manipulate_output(
    manipulation_func: Callable[[Any], Any], logger: logging.Logger | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to manipulate the output of a function using a specified manipulation function.

    Parameters
    ----------
    manipulation_func : Callable[[Any], Any]
        The function to manipulate the output of the decorated function.
    logger : logging.Logger | None
        The logger to use for logging manipulation warnings.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
        If the manipulation_func is not a callable function.
    """
    validate_logger(logger)
    if not callable(manipulation_func):
        if logger is not None:
            logger.error("manipulation_func must be a callable function.")
        raise TypeError("manipulation_func must be a callable function.")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be decorated.

        Returns
        -------
        Callable[P, R]
            The wrapped function.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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


__all__ = ["manipulate_output"]
