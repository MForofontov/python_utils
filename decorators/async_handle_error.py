from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import inspect
import logging
from logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def async_handle_error(
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """Decorator for handling errors in asynchronous functions.

    Parameters
    ----------
    logger : logging.Logger | None, optional
        Logger used to record errors. If ``None``, the exception is printed and
        re-raised.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A decorator that wraps an asynchronous function with error handling.

    Raises
    ------
    TypeError
        If ``logger`` is not an instance of :class:`logging.Logger` or ``None``.
    """
    validate_logger(logger)

    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
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
                logger.error(
                    f"An error occurred in {func.__name__}: {error_message}",
                    exc_info=True,
                )
            else:
                raise TypeError(error_message)

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
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
                The result of the wrapped function. If an exception occurs and a
                logger is provided, ``None`` is returned after logging. If no
                logger is provided, the error is printed and the exception is
                re-raised.
            """
            try:
                # Attempt to call the original asynchronous function
                return await func(*args, **kwargs)
            except Exception as e:
                # Log the error message and the exception if logging is enabled
                if logger:
                    logger.error(
                        f"An error occurred in {func.__name__}: {e}", exc_info=True
                    )
                    # Return None when logging the exception
                    return None
                # Print the custom error message and re-raise when no logger is provided
                print(f"An error occurred in {func.__name__}: {e}")
                raise

        return wrapper

    return decorator

__all__ = ['async_handle_error']
