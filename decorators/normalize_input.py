from typing import Any
from collections.abc import Callable
from functools import wraps
import logging
from logger_functions.logger import validate_logger


def normalize_input(
    normalization_func: Callable[[Any], Any], logger: logging.Logger | None = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to normalize the input arguments of a function using a specified normalization function.

    Parameters
    ----------
    normalization_func : Callable[[Any], Any]
        The function to normalize each input argument.
    logger : Optional[logging.Logger], optional
        The logger to use for logging normalization errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
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
            except Exception as e:
                message = f"Normalization failed: {e}"
                if logger:
                    logger.error(message, exc_info=True)
                raise TypeError(message)

            try:
                return func(*normalized_args, **normalized_kwargs)
            except Exception as e:
                if logger:
                    logger.error(str(e), exc_info=True)
                raise

        return wrapper

    return decorator
