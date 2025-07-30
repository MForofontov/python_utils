"""Utilities for creating module-specific loggers and validating logger instances."""

import logging
from logging import Logger, NullHandler


def get_logger(name: str = __name__) -> Logger:
    """Return a logger configured with :class:`~logging.NullHandler`."""
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
    """Validate that ``logger`` is a ``logging.Logger`` or ``None``.

    Parameters
    ----------
    logger : logging.Logger | None
        Logger instance to validate.
    allow_none : bool, optional
        Whether ``None`` is considered valid. Defaults to ``True``.
    message : str | None, optional
        Custom error message to raise if validation fails. If not provided, a
        default message is used based on ``allow_none``.
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
