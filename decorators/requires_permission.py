import logging
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from logger_functions.logger import validate_logger

P = ParamSpec("P")
R = TypeVar("R")


def requires_permission(
    permission: str, logger: logging.Logger | None = None
) -> Callable[
    [Callable[Concatenate[list[str], P], R]], Callable[Concatenate[list[str], P], R]
]:
    """
    A decorator to enforce that a user has a specific permission before executing a function.

    Parameters
    ----------
    permission : str
        The required permission that the user must have.
    logger : logging.Logger | None, optional
        The logger to use for logging errors (default is None).

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        The decorator function.

    Raises
    ------
    TypeError
        If logger is not an instance of logging.Logger or None.
    """
    validate_logger(logger)
    if not isinstance(permission, str):
        if logger:
            logger.error(
                "Type error in requires_permission decorator: permission must be a string",
                exc_info=True,
            )
        raise TypeError("permission must be a string")

    def decorator(
        func: Callable[Concatenate[list[str], P], R],
    ) -> Callable[Concatenate[list[str], P], R]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[P, R]
            The function to be decorated.

        Returns
        -------
        Callable[P, R]
            The wrapped function.
        """

        @wraps(func)
        def wrapper(
            user_permissions: list[str], *args: P.args, **kwargs: P.kwargs
        ) -> R:
            """
            The wrapper function that checks for the required permission.

            Parameters
            ----------
            user_permissions : list[str]
                The list of permissions that the user has.
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The result of the decorated function.

            Raises
            ------
            PermissionError
                If the user does not have the required permission.
            TypeError
                If user_permissions is not a list.
            """
            # Check if user_permissions is a list
            if not isinstance(user_permissions, list):
                error_message = "user_permissions must be a list."
                if logger:
                    logger.error(
                        f"Type error in {func.__name__}: {error_message}", exc_info=True
                    )
                raise TypeError(error_message)

            # Check if the required permission is in the user's permissions
            if permission not in user_permissions:
                permissions_str = repr(user_permissions)
                error_message = f"User does not have the required permission. Required permission: '{permission}', User permissions: {permissions_str}"
                if logger:
                    logger.error(
                        f"Permission error in {func.__name__}: {error_message}",
                        exc_info=True,
                    )
                raise PermissionError(error_message)
            # Call the original function with the provided arguments and keyword arguments
            return func(user_permissions, *args, **kwargs)

        return wrapper

    return decorator


__all__ = ["requires_permission"]
