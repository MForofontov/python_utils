from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
P = ParamSpec("P")
R = TypeVar("R")


def format_output(
    format_string: str,
) -> Callable[[Callable[P, R]], Callable[P, str]]:
    """
    A decorator to format the output of a function using a specified format string.

    Parameters
    ----------
    format_string : str
        The format string to use for formatting the output.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, str]]
        The decorator function.

    Raises
    ------
    TypeError
        If the format_string is not a string.
    """
    if not isinstance(format_string, str):
        raise TypeError("format_string must be a string")

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
            The wrapper function that formats the output of the decorated function.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            str
                The formatted output of the decorated function.
            """
            result = func(*args, **kwargs)
            return format_string.format(result)

        return wrapper

    return decorator


__all__ = ['format_output']
