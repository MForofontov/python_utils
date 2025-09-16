from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

T = TypeVar("T")


def chain(func: Callable[P, T]) -> Callable[P, T | Any]:
    """
    Decorator to call the 'chain' method on the result of a function if it exists.

    Parameters
    ----------
    func : Callable[P, T]
        The function to be wrapped.

    Returns
    -------
    Callable[P, T | Any]
        A wrapper function that calls the 'chain' method on the result of the input function if it exists.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | Any:
        """
        Wrapper function to call the 'chain' method on the result of the input function if it exists.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the wrapped function.
        **kwargs : Any
            Keyword arguments to pass to the wrapped function.

        Returns
        -------
        T | Any
            The result of the wrapped function, or the result of calling its 'chain' method if it exists.

        Raises
        ------
        RuntimeError
            If the 'chain' method raises an error.
        """
        result = func(*args, **kwargs)
        if hasattr(result, "chain") and callable(result.chain):
            chain_method = result.chain
            try:
                if not args and not kwargs:
                    sig = signature(chain_method)
                    required = [
                        p
                        for name, p in sig.parameters.items()
                        if name != "self"
                        and p.default is Parameter.empty
                        and p.kind
                        in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
                    ]
                    if not required:
                        return chain_method()
                else:
                    return chain_method(*args, **kwargs)
            except Exception as e:
                raise RuntimeError(
                    f"Error calling 'chain' method on result of {func.__name__}: {e}"
                )
        return result

    return wrapper


__all__ = ["chain"]
