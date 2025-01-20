from typing import Callable, Any
from functools import wraps
import time

def requires_permission(permission: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to enforce that a user has a specific permission before executing a function.

    Parameters
    ----------
    permission : str
        The required permission that the user must have.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to be decorated.

        Returns
        -------
        Callable[..., Any]
            The wrapped function.
        """
        @wraps(func)
        def wrapper(user_permissions: list[str], *args: Any, **kwargs: Any) -> Any:
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
            """
            # Check if the required permission is in the user's permissions
            if permission not in user_permissions:
                raise PermissionError("User does not have the required permission.")
            # Call the original function with the provided arguments and keyword arguments
            return func(*args, **kwargs)
        return wrapper
    return decorator
