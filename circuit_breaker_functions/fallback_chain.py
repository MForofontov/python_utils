"""
Fallback chain pattern for handling multiple fallback strategies.
"""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def fallback_chain(
    primary: Callable[[], T],
    fallbacks: list[Callable[[], T]],
    *args: Any,
    **kwargs: Any,
) -> T:
    """
    Execute function with multiple fallback strategies.

    Attempts to execute the primary function, falling back to a chain of
    alternative implementations if failures occur. This pattern provides
    graceful degradation when primary services are unavailable.

    Parameters
    ----------
    primary : Callable
        Primary function to attempt first.
    fallbacks : list[Callable]
        Ordered list of fallback functions to try.
    *args : Any
        Positional arguments passed to all functions.
    **kwargs : Any
        Keyword arguments passed to all functions.

    Returns
    -------
    T
        Result from the first successful function.

    Raises
    ------
    TypeError
        If primary or fallbacks are not callable.
    ValueError
        If fallbacks list is empty.
    Exception
        If all functions (primary and fallbacks) fail.

    Examples
    --------
    >>> def primary_api():
    ...     raise Exception("API down")
    >>> def fallback_cache():
    ...     return "cached_data"
    >>> def fallback_default():
    ...     return "default_data"
    >>> result = fallback_chain(primary_api, [fallback_cache, fallback_default])
    'cached_data'

    >>> # All succeed returns primary result
    >>> def primary_ok():
    ...     return "primary"
    >>> result = fallback_chain(primary_ok, [fallback_cache])
    'primary'

    Notes
    -----
    The fallback chain pattern implements graceful degradation by trying
    multiple strategies in order. This is useful for:
    - API calls with cache fallback
    - Primary database with read replica fallback
    - External service with local computation fallback

    Each function in the chain receives the same arguments.

    Complexity
    ----------
    Time: O(n) where n is number of functions, Space: O(1)
    """
    # Type validation
    if not callable(primary):
        raise TypeError(f"primary must be callable, got {type(primary).__name__}")

    if not isinstance(fallbacks, list):
        raise TypeError(f"fallbacks must be a list, got {type(fallbacks).__name__}")

    if not fallbacks:
        raise ValueError("fallbacks list cannot be empty")

    if not all(callable(f) for f in fallbacks):
        raise TypeError("all items in fallbacks must be callable")

    # Track all errors for final exception
    errors: list[Exception] = []

    # Try primary function
    try:
        return primary(*args, **kwargs)
    except Exception as e:
        errors.append(e)

    # Try fallbacks in order
    for i, fallback_func in enumerate(fallbacks):
        try:
            return fallback_func(*args, **kwargs)
        except Exception as e:
            errors.append(e)

    # All functions failed
    error_messages = "\n".join(
        [f"  {i}. {type(e).__name__}: {e}" for i, e in enumerate(errors)]
    )
    raise Exception(
        f"All functions in fallback chain failed ({len(errors)} attempts):\n{error_messages}"
    )


class FallbackChain:
    """
    Reusable fallback chain with configured strategies.

    Attributes
    ----------
    primary : Callable
        Primary function to attempt.
    fallbacks : list[Callable]
        Ordered list of fallback functions.

    Parameters
    ----------
    primary : Callable
        Primary function to attempt first.
    fallbacks : list[Callable]
        Ordered list of fallback functions.

    Raises
    ------
    TypeError
        If primary or fallbacks are not callable.
    ValueError
        If fallbacks list is empty.

    Examples
    --------
    >>> def primary_db():
    ...     return "primary_data"
    >>> def replica_db():
    ...     return "replica_data"
    >>> def cache():
    ...     return "cached_data"
    >>> chain = FallbackChain(primary_db, [replica_db, cache])
    >>> result = chain.execute()
    'primary_data'

    Notes
    -----
    Use this class when you have a reusable fallback strategy that
    will be executed multiple times with the same fallback order.

    Complexity
    ----------
    Time: O(n) per execution, Space: O(n) for fallback storage
    """

    def __init__(
        self,
        primary: Callable[[], T],
        fallbacks: list[Callable[[], T]],
    ) -> None:
        """Initialize fallback chain with primary and fallback functions."""
        if not callable(primary):
            raise TypeError(f"primary must be callable, got {type(primary).__name__}")

        if not isinstance(fallbacks, list):
            raise TypeError(
                f"fallbacks must be a list, got {type(fallbacks).__name__}"
            )

        if not fallbacks:
            raise ValueError("fallbacks list cannot be empty")

        if not all(callable(f) for f in fallbacks):
            raise TypeError("all items in fallbacks must be callable")

        self.primary = primary
        self.fallbacks = fallbacks

    def execute(self, *args: Any, **kwargs: Any) -> T:  # type: ignore[type-var]
        """
        Execute the fallback chain.

        Parameters
        ----------
        *args : Any
            Positional arguments passed to all functions.
        **kwargs : Any
            Keyword arguments passed to all functions.

        Returns
        -------
        T
            Result from the first successful function.

        Raises
        ------
        Exception
            If all functions fail.

        Examples
        --------
        >>> chain = FallbackChain(lambda: "a", [lambda: "b"])
        >>> chain.execute()
        'a'
        """
        return fallback_chain(self.primary, self.fallbacks, *args, **kwargs)  # type: ignore[return-value]

    def add_fallback(self, fallback: Callable[[], T]) -> None:
        """
        Add an additional fallback to the end of the chain.

        Parameters
        ----------
        fallback : Callable
            Fallback function to add.

        Raises
        ------
        TypeError
            If fallback is not callable.

        Examples
        --------
        >>> chain = FallbackChain(lambda: "a", [lambda: "b"])
        >>> chain.add_fallback(lambda: "c")
        >>> len(chain.fallbacks)
        2
        """
        if not callable(fallback):
            raise TypeError(f"fallback must be callable, got {type(fallback).__name__}")
        self.fallbacks.append(fallback)  # type: ignore[arg-type]


__all__ = ["fallback_chain", "FallbackChain"]
