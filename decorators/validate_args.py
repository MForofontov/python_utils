import logging
from typing import Any
from collections.abc import Callable
from functools import wraps

def validate_args(validation_func: Callable[..., bool], logger: logging.Logger | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator that validates the arguments of a function using a provided validation function.

    Parameters
    ----------
    validation_func : Callable[..., bool]
        The validation function that takes the same arguments as the decorated function and returns a boolean.
    logger : Optional[logging.Logger]
        The logger to use for logging validation failure messages. If None, messages are printed to the console.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    
    Raises
    ------
    TypeError
        If validation_func is not callable or if logger is not an instance of logging.Logger or None.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")
    if not callable(validation_func):
        if logger:
            logger.error(f"Validation function {validation_func} is not callable", exc_info=True)
        raise TypeError("validation_func must be callable")

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
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that validates the arguments.

            Parameters
            ----------
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
            ValueError
                If the arguments do not pass the validation function.
            """
            # Validate the arguments using the provided validation function
            if not validation_func(*args, **kwargs):
                message = f"Function {func.__name__} arguments did not pass validation."
                if logger:
                    logger.error(message)
                raise ValueError(message)
            # Call the original function with the validated arguments
            return func(*args, **kwargs)
        return wrapper
    return decorator
