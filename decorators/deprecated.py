from typing import Any, ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import warnings
import logging
from logger_functions.logger import validate_logger
P = ParamSpec("P")
R = TypeVar("R")


def deprecated(
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to mark functions as deprecated. It will result in a warning being emitted when the function is used.

    Parameters
    ----------
    logger : Optional[logging.Logger]
        The logger to use for logging the deprecation warning. If None, the default logger will be used.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        A decorator that wraps the input function with deprecation warning logic.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator function to wrap the input function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be marked as deprecated.

        Returns
        -------
        Callable[P, R]
            A wrapper function that emits a deprecation warning when the input function is called.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            Wrapper function to emit a deprecation warning and log a message.

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
            # Log the deprecation warning
            if logger is not None:
                logger.warning(
                    f"Call to deprecated function {func.__name__}.", exc_info=True
                )
            # Emit a deprecation warning
            else:
                warnings.warn(
                    f"{func.__name__} is deprecated.", DeprecationWarning, stacklevel=2
                )
            # Call the original function and return its result
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ['deprecated']
