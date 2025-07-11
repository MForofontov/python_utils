from typing import Any
from collections.abc import Callable
import logging

def multi_decorator(decorators: list[Callable[[Callable[..., Any]], Callable[..., Any]]], logger: logging.Logger | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A function to apply multiple decorators to a target function.

    Parameters
    ----------
    decorators : List[Callable[[Callable[..., Any]], Callable[..., Any]]]
        A list of decorators to apply.
    logger : Optional[logging.Logger], optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The function that applies all the decorators to the target function.
    
    Raises
    ------
    TypeError
        If any of the decorators are not callable or if logger is not an instance of logging.Logger or None.
    """
    for decorator in decorators:
        if not callable(decorator):
            message = f"Decorator {decorator} is not callable"
            if logger:
                logger.error(message, exc_info=True)
            raise TypeError(message)
    
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")

    def combine(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The function that applies all the decorators to the target function.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to be decorated.

        Returns
        -------
        Callable[..., Any]
            The decorated function.
        """
        for decorator in reversed(decorators):
            func = decorator(func)
        return func

    return combine
