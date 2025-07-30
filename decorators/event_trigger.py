from typing import Any
from collections.abc import Callable
from functools import wraps
import logging
from logger_functions.logger import validate_logger


class EventManager:
    """
    A class to manage events and their associated callbacks.

    Attributes
    ----------
    events : Dict[str, List[Callable[..., Any]]]
        A dictionary where the keys are event names and the values are lists of callback functions.

    Methods
    -------
    __init__():
        Initializes the EventManager with an empty events dictionary.
    subscribe(event_name: str, callback: Callable[..., Any]):
        Adds a callback function to the list of callbacks for a given event name.
    trigger(event_name: str, *args: Any, **kwargs: Any):
        Executes all callback functions associated with the given event name
        using the provided arguments.
    """

    def __init__(self):
        """
        Initializes the EventManager with an empty events dictionary.
        """
        self.events: dict[str, list[Callable[..., Any]]] = {}

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        """
        Adds a callback function to the list of callbacks for a given event name.

        Parameters
        ----------
        event_name : str
            The name of the event.
        callback : Callable[..., Any]
            The callback function to be added.
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def trigger(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Executes all callback functions associated with the given event name.

        Parameters
        ----------
        event_name : str
            The name of the event.
        *args : Any
            Positional arguments forwarded to the callbacks.
        **kwargs : Any
            Keyword arguments forwarded to the callbacks.
        """
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(*args, **kwargs)


def event_trigger(
    event_manager: EventManager, event_name: str, logger: logging.Logger | None = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to trigger an event before executing the decorated function.

    Parameters
    ----------
    event_manager : EventManager
        The event manager to use for triggering events.
    event_name : str
        The name of the event to trigger.
    logger : Optional[logging.Logger]
        The logger to use for logging errors.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.

    Raises
    ------
    TypeError
        If any of the parameters do not match the expected types.
    """

    def log_or_raise_error(message: str) -> None:
        """
        Helper function to log an error or raise an exception.

        Parameters
        ----------
        message : str
            The error message to log or raise.
        """
        if logger:
            logger.error(message, exc_info=True)
        raise TypeError(message)

    validate_logger(logger)

    if not isinstance(event_manager, EventManager):
        log_or_raise_error("event_manager must be an instance of EventManager")

    if not isinstance(event_name, str) or not event_name:
        log_or_raise_error("event_name must be a non-empty string")

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
            The wrapper function that triggers the event and then calls the original function.

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
            event_manager.trigger(event_name, *args, **kwargs)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(str(e), exc_info=True)
                raise

        return wrapper

    return decorator

__all__ = ['EventManager', 'event_trigger']
