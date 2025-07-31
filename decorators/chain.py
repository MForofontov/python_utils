from typing import Any, TypeVar
from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature

T = TypeVar("T")


def chain(func: Callable[..., T]) -> Callable[..., T | Any]:
    """
    Decorator to call the 'chain' method on the result of a function if it exists.

    Parameters
    ----------
    func : Callable[..., T]
        The function to be wrapped.

    Returns
    -------
    Callable[..., Union[T, Any]]
        A wrapper function that calls the 'chain' method on the result of the input function if it exists.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T | Any:
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
        Union[T, Any]
            The result of the wrapped function, or the result of calling its 'chain' method if it exists.

        Raises
        ------
        RuntimeError
            If the 'chain' method raises an error.
        """
        result = func(*args, **kwargs)
        if hasattr(result, "chain") and callable(getattr(result, "chain")):
            chain_method = getattr(result, "chain")
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

__all__ = ['chain']
