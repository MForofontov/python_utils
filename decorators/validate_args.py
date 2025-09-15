import logging
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
from logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def validate_args(
    validation_func: Callable[P, bool], logger: logging.Logger | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator that validates the arguments of a function using a provided validation function.

    Parameters
    ----------
    validation_func : Callable[P, bool]
        The validation function that takes the same arguments as the decorated function and returns a boolean.
    logger : logging.Logger | None
        The logger to use for logging validation failure messages. If None, messages are printed to the console.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The decorator function.

    Raises
    ------
    TypeError
        If validation_func is not callable or if logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)
    if not callable(validation_func):
        if logger:
            logger.error(
                f"Validation function {validation_func} is not callable", exc_info=True
            )
        raise TypeError("validation_func must be callable")

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
            The wrapper function that validates the arguments.

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
            ValueError
                If the arguments do not pass the validation function.
            """
            # Validate the arguments using the provided validation function
            if not validation_func(*args, **kwargs):
                message = f"Function {func.__name__} arguments did not pass validation."
                if logger:
                    logger.error(message)
                raise ValueError(message)
            # Call the original function with the validated arguments
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["validate_args"]
