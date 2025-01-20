from typing import Callable, Any
from functools import wraps
import json
import logging

def serialize_output(format: str, logger: logging.Logger = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to serialize the output of a function into a specified format.

    Parameters
    ----------
    format : str
        The format to serialize the output into. Currently supports 'json'.
    logger : logging.Logger, optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    ValueError
        If the format is not supported.
    TypeError
        If logger is not an instance of logging.Logger or
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")

    if not isinstance(format, str):
        if logger:
            logger.error("Type error in serialize_output decorator: format must be a string.", exc_info=True)
        raise TypeError("format must be a string.")

    if format not in ['json']:
        if logger:
            logger.error("Value error in serialize_output decorator: Unsupported format.", exc_info=True)
        raise ValueError("Unsupported format. Currently, only 'json' is supported.")

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
        def wrapper(*args: Any, **kwargs: Any) -> str:
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
                if format == 'json':
                    return json.dumps(result)
            except Exception as e:
                if logger:
                    logger.error(f"Error serializing output in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator