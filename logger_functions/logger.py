"""Module-specific loggers and logger instance validation."""

import logging
from logging import Logger, NullHandler


def get_logger(name: str = __name__) -> Logger:
    """
    Return a logger configured with :class:`~logging.NullHandler`.

    Parameters
    ----------
    name : str, optional
        Name of the logger to retrieve. Defaults to ``__name__``.

    Returns
    -------
    Logger
        Logger instance equipped with a ``NullHandler``.

    Raises
    ------
    None

    Examples
    --------
    >>> from logging import Logger
    >>> logger = get_logger('my_module')
    >>> isinstance(logger, Logger)
    True
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(NullHandler())
    return logger


def validate_logger(
    logger: Logger | None,
    *,
    allow_none: bool = True,
    message: str | None = None,
) -> None:
    """
    Validate that ``logger`` is a ``logging.Logger`` or ``None``.

    Parameters
    ----------
    logger : logging.Logger | None
        Logger instance to validate.
    allow_none : bool, optional
        Whether ``None`` is considered valid. Defaults to ``True``.
    message : str | None, optional
        Custom error message to raise if validation fails. If not provided, a
        default message is constructed based on ``allow_none``.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If ``logger`` is not a ``logging.Logger`` instance and ``allow_none`` is
        ``False``.

    Examples
    --------
    >>> validate_logger(get_logger('test'))
    >>> validate_logger('not_logger', allow_none=False)
    Traceback (most recent call last):
    ...
    TypeError: logger must be an instance of logging.Logger or None.
    """
    valid = isinstance(logger, Logger) or (allow_none and logger is None)
    if not valid:
        if message is None:
            message = "logger must be an instance of logging.Logger"
            if allow_none:
                message += " or None"
            message += "."
        raise TypeError(message)


module_logger = get_logger(__name__)

__all__ = ["get_logger", "validate_logger"]
