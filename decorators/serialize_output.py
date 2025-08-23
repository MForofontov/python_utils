from typing import Any, ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import json
import logging
from logger_functions.logger import validate_logger
P = ParamSpec("P")
R = TypeVar("R")


def serialize_output(
    format: str, logger: logging.Logger | None = None
) -> Callable[[Callable[P, R]], Callable[P, str]]:
    """
    A decorator to serialize the output of a function into a specified format.

    Parameters
    ----------
    format : str
        The format to serialize the output into. Currently supports 'json'.
    logger : Optional[logging.Logger], optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, str]]
        The decorator function.

    Raises
    ------
    ValueError
        If the format is not supported.
    TypeError
        If logger is not an instance of logging.Logger or None.
    """
    try:
        validate_logger(logger)
    except TypeError:
        logger = None

    if not isinstance(format, str):
        if logger:
            logger.error(
                "Type error in serialize_output decorator: format must be a string.",
                exc_info=True,
            )
        raise TypeError("format must be a string.")

    if format not in ["json"]:
        if logger:
            logger.error(
                "Value error in serialize_output decorator: Unsupported format.",
                exc_info=True,
            )
        raise ValueError(
            "Unsupported format. Currently, only 'json' is supported.")

    def decorator(func: Callable[P, R]) -> Callable[P, str]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be decorated.

        Returns
        -------
        Callable[P, str]
            The wrapped function.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            """
            The wrapper function that serializes the output.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            str
                The serialized output of the decorated function.
            """
            try:
                result = func(*args, **kwargs)
                return json.dumps(result)
            except Exception as e:
                if logger:
                    logger.error(
                        f"Error serializing output in {func.__name__}: {e}",
                        exc_info=True,
                    )
                raise

        return wrapper

    return decorator


__all__ = ['serialize_output']
