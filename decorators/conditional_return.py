from typing import Any, TypeVar
from collections.abc import Callable
from functools import wraps

T = TypeVar("T")


def conditional_return(
    condition: Callable[..., bool], return_value: T
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to conditionally return a specified value based on a condition.

    Parameters
    ----------
    condition : Callable[..., bool]
        A function that returns a boolean value. The decorated function will return the specified value if this condition returns True.
    return_value : T
        The value to return if the condition is met.

    Returns
    -------
    Callable[[Callable[..., T]], Callable[..., T]]
        A decorator that wraps the input function with conditional return logic.

    Raises
    ------
    TypeError
        If the condition is not callable.
    """
    if not callable(condition):
        raise TypeError("Condition must be callable")

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator function.

        Parameters
        ----------
        func : Callable[..., T]
            The function to be conditionally executed.

        Returns
        -------
        Callable[..., T]
            The wrapped function with conditional return logic.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            """
            Wrapper function to conditionally return a specified value.

            Parameters
            ----------
            *args : Any
                Positional arguments to pass to the wrapped function.
            **kwargs : Any
                Keyword arguments to pass to the wrapped function.

            Returns
            -------
            T
                The specified return value if the condition is met, otherwise the result of the wrapped function.

            Raises
            ------
            RuntimeError
                If the condition function raises an error.
            """
            try:
                if condition(*args, **kwargs):
                    return return_value
            except Exception as e:
                raise RuntimeError(f"Condition function raised an error: {e}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
