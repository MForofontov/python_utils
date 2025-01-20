from typing import Callable, Any
from functools import wraps
import json

def serialize_output(format: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to serialize the output of a function into a specified format.

    Parameters
    ----------
    format : str
        The format to serialize the output into. Currently supports 'json'.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    """
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
            # Call the original function and get the result
            result = func(*args, **kwargs)
            # Serialize the result based on the specified format
            if format == 'json':
                return json.dumps(result)
            # Default to converting the result to a string
            return str(result)
        return wrapper
    return decorator
