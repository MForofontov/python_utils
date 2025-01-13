import os
import logging
from typing import Callable, Optional, Any, Type

def env_config(var_name: str, logger: Optional[logging.Logger] = None, 
               default: Optional[Any] = None, required: bool = False, 
               var_type: Type = str, custom_message: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to check for an environment variable before executing the function.

    Parameters
    ----------
    var_name : str
        The name of the environment variable to check.
    logger : Optional[logging.Logger]
        The logger to use for logging the environment variable value.
    default : Optional[Any]
        The default value to use if the environment variable is not set.
    required : bool
        Whether the environment variable is required. Logs an error if not set.
    var_type : Type
        The type to convert the environment variable value to.
    custom_message : Optional[str]
        A custom message to log instead of the default message.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If any of the parameters do not match the expected types.
    """
    def log_or_raise_error(message: str):
        """
        Helper function to log an error or raise an exception.
        """
        if logger:
            logger.error(message, exc_info=True)
            return None
        else:
            raise TypeError(message)

    if not isinstance(logger, logging.Logger) and logger is not None:
        raise TypeError("logger must be an instance of logging.Logger or None")

    if not isinstance(var_name, str) or not var_name:
        log_or_raise_error("var_name must be a non-empty string")
    
    if not isinstance(required, bool):
        log_or_raise_error("required must be a boolean")
    
    if not isinstance(var_type, type):
        log_or_raise_error("var_type must be a type")
    
    if not isinstance(custom_message, str) and custom_message is not None:
        log_or_raise_error("custom_message must be a string or None")

    
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
            The wrapper function that checks the environment variable.

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
            if var_name in os.environ:
                value = os.environ[var_name]
                try:
                    value = var_type(value)
                except ValueError:
                    error_message = f"Environment variable {var_name} cannot be converted to {var_type.__name__}"
                    if logger:
                        logger.error(error_message)
                    else:
                        raise ValueError(error_message)
                    return None
                message = custom_message or f"Using environment variable {var_name} with value: {value}"
                if logger:
                    logger.info(message)
                else:
                    print(message)
            else:
                if required:
                    error_message = f"Required environment variable {var_name} is not set"
                    if logger:
                        logger.error(error_message)
                    else:
                        raise ValueError(error_message)
                    return None
                value = default
                if value is not None:
                    message = custom_message or f"Using default value for {var_name}: {value}"
                    if logger:
                        logger.info(message)
                    else:
                        print(message)
            return func(*args, **kwargs, env_var_value=value)
        return wrapper
    
    return decorator
