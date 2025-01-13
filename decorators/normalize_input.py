from typing import Callable, Any

def normalize_input(normalization_func: Callable[[Any], Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to normalize the input arguments of a function using a specified normalization function.

    Parameters
    ----------
    normalization_func : Callable[[Any], Any]
        The function to normalize each input argument.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    
    Raises
    ------
    TypeError
        If the input function is not callable.
    """
    if not callable(normalization_func):
        raise TypeError(f"Normalizer {normalization_func} is not callable")

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
            The wrapper function that normalizes the input arguments.

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
            """
            normalized_args = tuple(normalization_func(arg) for arg in args)
            normalized_kwargs = {k: normalization_func(v) for k, v in kwargs.items()}
            return func(*normalized_args, **normalized_kwargs)

        return wrapper
    return decorator