"""Input normalization decorator."""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from pyutils_collection.logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def normalize_input(
    normalization_func: Callable[[Any], Any], logger: logging.Logger | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to normalize the input arguments of a function using a specified normalization function.

    Parameters
    ----------
    normalization_func : Callable[[Any], Any]
        The function to normalize each input argument.
    logger : logging.Logger | None, optional
        The logger to use for logging normalization errors (default is None).

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The decorator function.

    Raises
    ------
    TypeError
        If the input function is not callable or if logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)
    if not callable(normalization_func):
        if logger:
            logger.error(
                f"Normalizer {normalization_func} is not callable", exc_info=True
            )
        raise TypeError(f"Normalizer {normalization_func} is not callable")

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
            The wrapper function that normalizes the input arguments.

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
            try:
                normalized_args = tuple(normalization_func(arg) for arg in args)
                normalized_kwargs = {
                    k: normalization_func(v) for k, v in kwargs.items()
                }
            except Exception as exc:
                message = f"Normalization failed: {exc}"
                if logger:
                    logger.error(message, exc_info=True)
                raise TypeError(message) from exc

            try:
                return func(*normalized_args, **normalized_kwargs)
            except Exception as exc:
                if logger:
                    logger.error(str(exc), exc_info=True)
                raise

        return wrapper

    return decorator


__all__ = ["normalize_input"]
