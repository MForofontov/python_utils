from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import inspect
import logging
from logger_functions.logger import validate_logger
P = ParamSpec("P")
R = TypeVar("R")


def log_signature(
    logger: logging.Logger | None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to log the function signature and the arguments passed to it.

    Parameters
    ----------
    logger : logging.Logger | None
        The logger to use for logging. If None, a default logger is used.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger.
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    validate_logger(logger, allow_none=False)

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
            The wrapper function that logs the function signature and arguments.

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
            Exception
                If an exception is raised in the decorated function
            """
            signature = inspect.signature(func)
            logger.info(
                f"Executing {func.__name__}{signature} with args: {args} and kwargs: {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} returned: {result}")
                return result
            except Exception:
                logger.exception(
                    f"Exception occurred in {func.__name__}():"
                )
                raise

        return wrapper

    return decorator


__all__ = ['log_signature']
