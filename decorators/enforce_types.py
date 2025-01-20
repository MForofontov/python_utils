import logging
from functools import wraps
from typing import Callable, Any, get_type_hints, Optional

def enforce_types(logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to enforce type checking on the arguments and return value of a function.

    Parameters
    ----------
    logger : Optional[logging.Logger]
        The logger to use for logging type errors.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    
    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
    """
    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")
    
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
            The wrapper function that checks the types of the arguments and return value.

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
            TypeError
                If an argument or return value does not match the expected type.
            """
            hints = get_type_hints(func)
            for arg_name, arg_value in zip(hints.keys(), args):
                expected_type = hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    error_message = f"Expected {expected_type} for argument '{arg_name}', got {type(arg_value)}."
                    if logger:
                        logger.error(error_message, exc_info=True)
                    raise TypeError(error_message)
            for arg_name, arg_value in kwargs.items():
                if arg_name in hints:
                    expected_type = hints[arg_name]
                    if not isinstance(arg_value, expected_type):
                        error_message = f"Expected {expected_type} for argument '{arg_name}', got {type(arg_value)}."
                        if logger:
                            logger.error(error_message, exc_info=True)
                        raise TypeError(error_message)
            result = func(*args, **kwargs)
            if 'return' in hints:
                expected_return_type = hints['return']
                if not isinstance(result, expected_return_type):
                    error_message = f"Expected return type {expected_return_type}, got {type(result)}."
                    if logger:
                        logger.error(error_message, exc_info=True)
                    raise TypeError(error_message)
            return result

        return wrapper

    return decorator
