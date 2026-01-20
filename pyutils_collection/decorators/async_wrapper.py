"""Async function wrapper decorator."""

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from functools import partial, wraps
from typing import ParamSpec, TypeVar

from python_utils.logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def async_wrapper(
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R | None]]]:
    """
    Wraps a synchronous function to be executed asynchronously.

    Parameters
    ----------
    logger : logging.Logger | None
        The logger to use for logging errors. If None, the default logger will be used.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, Awaitable[R | None]]]
        A decorator that wraps a synchronous function in an async wrapper.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    validate_logger(
        logger,
        message="The logger must be an instance of logging.Logger",
    )

    def decorator(func: Callable[P, R]) -> Callable[P, Awaitable[R | None]]:
        """
        Decorator function.

        Parameters
        ----------
        func : Callable[P, R]
            The synchronous function to be wrapped.

        Returns
        -------
        Callable[P, Awaitable[R | None]]
            The wrapped function with asynchronous execution.

        Raises
        ------
        TypeError
            If the function is asynchronous.
        """
        if inspect.iscoroutinefunction(func):
            error_message = "The function to be wrapped must be synchronous"
            if logger:
                logger.error(
                    f"An error occurred in {func.__name__}: {error_message}",
                    exc_info=True,
                )
            raise TypeError(error_message)

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
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
                partial_func = partial(func, *args, **kwargs)
                return await loop.run_in_executor(None, partial_func)
            except Exception as e:
                if logger:
                    logger.error(
                        f"An error occurred in {func.__name__}: {e}", exc_info=True
                    )
                    return None
                else:
                    raise

        return wrapper

    return decorator  # Return the decorator instead of the wrapper itself


__all__ = ["async_wrapper"]
