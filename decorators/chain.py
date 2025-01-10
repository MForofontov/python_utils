from typing import Callable, Any, TypeVar, Union

T = TypeVar('T')

def chain(func: Callable[..., T]) -> Callable[..., Union[T, Any]]:
    """
    Decorator to call the 'chain' method on the result of a function if it exists.

    Parameters
    ----------
    func : Callable[..., T]
        The function to be wrapped.

    Returns
    -------
    Callable[..., Union[T, Any]]
        A wrapper function that calls the 'chain' method on the result of the input function if it exists.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Union[T, Any]:
        """
        Wrapper function to call the 'chain' method on the result of the input function if it exists.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the wrapped function.
        **kwargs : Any
            Keyword arguments to pass to the wrapped function.

        Returns
        -------
        Union[T, Any]
            The result of the wrapped function, or the result of calling its 'chain' method if it exists.
        
        Raises
        ------
        RuntimeError
            If the 'chain' method raises an error.
        """
        result = func(*args, **kwargs)
        if hasattr(result, 'chain') and callable(getattr(result, 'chain')):
            try:
                return result.chain()
            except Exception as e:
                raise RuntimeError(f"Error calling 'chain' method on result of {func.__name__}: {e}")
        return result
    
    return wrapper