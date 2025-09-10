from typing import TypeVar, ParamSpec
from collections.abc import Callable
from functools import wraps
P = ParamSpec("P")
R = TypeVar("R")

T = TypeVar("T")


def conditional_return(
    condition: Callable[P, bool], return_value: T
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to conditionally return a specified value based on a condition.

    Parameters
    ----------
    condition : Callable[P, bool]
        A function that returns a boolean value. The decorated function will return the specified value if this condition returns True.
    return_value : T
        The value to return if the condition is met.

    Returns
    -------
    Callable[[Callable[P, T]], Callable[P, T]]
        A decorator that wraps the input function with conditional return logic.

    Raises
    ------
    TypeError
        If the condition is not callable.
    """
    if not callable(condition):
        raise TypeError("Condition must be callable")

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        """
        Decorator function.

        Parameters
        ----------
        func : Callable[P, T]
            The function to be conditionally executed.

        Returns
        -------
        Callable[P, T]
            The wrapped function with conditional return logic.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
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


__all__ = ['conditional_return']
