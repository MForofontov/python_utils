from typing import Callable, Any, Type
from functools import wraps

def validate_input(expected_type: Type) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to validate the type of the input argument of a function.

    Parameters
    ----------
    expected_type : Type
        The expected type of the input argument.

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
        def wrapper(arg: Any) -> Any:
            """
            The wrapper function that validates the input argument type.

            Parameters
            ----------
            arg : Any
                The input argument to be validated.

            Returns
            -------
            Any
                The result of the decorated function.

            Raises
            ------
            ValueError
                If the input argument is not of the expected type.
            """
            # Check if the argument is of the expected type
            if not isinstance(arg, expected_type):
                raise ValueError(f"Expected argument of type {expected_type}, got {type(arg)}")
            # Call the original function with the validated argument
            return func(arg)
        return wrapper
    return decorator