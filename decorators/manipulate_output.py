from typing import Callable, Any, Optional
import logging

def manipulate_output(manipulation_func: Callable[[Any], Any], logger: Optional[logging.Logger] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to manipulate the output of a function using a specified manipulation function.

    Parameters
    ----------
    manipulation_func : Callable[[Any], Any]
        The function to manipulate the output of the decorated function.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If the logger is not an instance of logging.Logger or None.
        If the manipulation_func is not a callable function.
    """
    if isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None.")
    if not callable(manipulation_func):
        if logger is not None:
            logger.error("manipulation_func must be a callable function.")
        else:
            raise TypeError("manipulation_func must be a callable function.")

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
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that manipulates the output of the decorated function.

            Parameters
            ----------
            *args : Any
                Positional arguments for the decorated function.
            **kwargs : Any
                Keyword arguments for the decorated function.

            Returns
            -------
            Any
                The manipulated output of the decorated function.
            """
            result = func(*args, **kwargs)
            return manipulation_func(result)
        return wrapper
    return decorator
