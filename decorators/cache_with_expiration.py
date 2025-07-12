from typing import Callable, Any, Dict, Tuple, FrozenSet
from functools import wraps
import time

def cache_with_expiration(expiration_time: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to cache the results of a function call for a specified amount of time.

    Parameters
    ----------
    expiration_time : int
        The time in seconds for which the cached result is valid.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    
    Raises
    ------
    ValueError
        If `expiration_time` is not a positive integer.
    """
    if not isinstance(expiration_time, int) or expiration_time < 0:
        raise ValueError("expiration_time must be a positive integer")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to be decorated.

        Returns
        -------
        Callable[..., Any]]
            The wrapped function.
        """
        cached_results: Dict[Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]], Tuple[float, Any]] = {}

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that caches the result of the decorated function.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The result of the decorated function, either from the cache or freshly computed.
            
            Raises
            ------
            TypeError
                If the arguments are unhashable
            """
            try:
                # Create a key based on the function arguments
                key: Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]] = (args, frozenset(kwargs.items()))

                current_time = time.time()
                if key in cached_results:
                    cached_time, cached_value = cached_results[key]
                    if current_time - cached_time < expiration_time:
                        return cached_value
                result = func(*args, **kwargs)
                cached_results[key] = (current_time, result)
            except TypeError as e:
                raise TypeError(f"Unhashable arguments: {e}")

            return result

        def cache_clear():
            """
            Clear the cache.
            """
            cached_results.clear()

        wrapper.cache_clear = cache_clear

        return wrapper
    return decorator
