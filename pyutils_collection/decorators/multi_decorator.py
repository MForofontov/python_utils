"""Multiple decorator composition utility."""

import logging
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from python_utils.logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def multi_decorator(
    decorators: list[Callable[[Callable[P, R]], Callable[P, R]]],
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A function to apply multiple decorators to a target function.

    Parameters
    ----------
    decorators : list[Callable[[Callable[P, R]], Callable[P, R]]]
        A list of decorators to apply.
    logger : logging.Logger | None, optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
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

    validate_logger(logger)

    def combine(func: Callable[P, R]) -> Callable[P, R]:
        """
        The function that applies all the decorators to the target function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be decorated.

        Returns
        -------
        Callable[P, R]
            The decorated function.
        """
        for decorator in reversed(decorators):
            func = decorator(func)
        return func

    return combine


__all__ = ["multi_decorator"]
