from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")


def cache(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to cache the results of a function call.

    Parameters
    ----------
    func : Callable[P, R]
        The function to be cached.

    Returns
    -------
    Callable[P, R]
        A wrapper function that caches the results of the input function.

    Raises
    ------
    TypeError
        If the decorated function is later called with unhashable arguments.

    Examples
    --------
    >>> @cache
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    >>> add(1, 2)
    3
    >>> add(1, 2)  # Cached result
    3
    >>> add.cache_clear()
    """

    cached_results: dict[tuple[tuple[Any, ...], frozenset[tuple[str, Any]]], Any] = {}

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """
        Wrapper function to cache the results of the input function.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the wrapped function.
        **kwargs : Any
            Keyword arguments to pass to the wrapped function.

        Returns
        -------
        Any
            The cached result of the wrapped function.

        Raises
        ------
        TypeError
            If the arguments are unhashable.
        """
        try:
            # Create a key based on the function arguments
            key: tuple[tuple[Any, ...], frozenset[tuple[str, Any]]] = (
                args,
                frozenset(kwargs.items()),
            )

            # Check if the result is already cached
            if key not in cached_results:
                # If not cached, call the function and store the result
                cached_results[key] = func(*args, **kwargs)
        except TypeError as exc:
            raise TypeError(f"Unhashable arguments: {exc}") from exc

        # Return the cached result
        return cached_results[key]

    def cache_clear() -> None:
        """Public method to clear the cached results for ``func``."""
        cached_results.clear()

    wrapper.cache_clear = cache_clear

    return cast(Callable[P, R], wrapper)


__all__ = ["cache"]
