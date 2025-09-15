"""
Contextual logger with built-in context support.

Automatically includes contextual information in all log messages.
"""

import logging
import threading
from contextlib import contextmanager
from typing import Any
from dataclasses import dataclass, field


@dataclass
class LogContext:
    """
    Context information for logging.

    Stores contextual information that can be included in log messages.
    """

    context_id: str = ""
    user_id: str = ""
    session_id: str = ""
    request_id: str = ""
    component: str = ""
    operation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            k: v
            for k, v in self.__dict__.items()
            if v or k == "metadata"  # Include metadata even if empty
        }

    def update(self, **kwargs) -> None:
        """Update context with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.metadata[key] = value


def contextual_logger(
    name: str, context: LogContext | None = None
) -> "ContextualLogger":
    """
    Create a logger with built-in context support.

    Parameters
    ----------
    name : str
        Logger name
    context : LogContext, optional
        Initial context information

    Returns
    -------
    ContextualLogger
        Configured contextual logger

    Examples
    --------
    >>> logger = contextual_logger('my_app', LogContext(user_id='123'))
    >>> logger.info('User action performed')
    """
    return ContextualLogger(name, context)


class ContextualLogger:
    """
    Logger with built-in context support.

    Automatically includes contextual information in all log messages.
    """

    def __init__(self, name: str, context: LogContext | None = None):
        self.logger = logging.getLogger(name)
        self.context = context or LogContext()
        self._local = threading.local()

    def _get_context(self) -> LogContext:
        """Get current context (thread-local or instance)."""
        if hasattr(self._local, "context"):
            return self._local.context
        return self.context

    def _set_context(self, context: LogContext) -> None:
        """Set thread-local context."""
        self._local.context = context

    @contextmanager
    def context_scope(self, **kwargs):
        """
        Context manager for temporary context changes.

        Parameters
        ----------
        **kwargs
            Context fields to temporarily set
        """
        old_context = self._get_context()
        new_context = LogContext(**old_context.to_dict())
        new_context.update(**kwargs)

        self._set_context(new_context)
        try:
            yield
        finally:
            self._set_context(old_context)

    def _log_with_context(
        self, level: int, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log message with current context."""
        context = self._get_context()

        # Merge context with extra data
        log_extra = context.to_dict()
        if extra:
            log_extra.update(extra)
        if kwargs:
            log_extra.update(kwargs)

        self.logger.log(level, message, extra=log_extra)

    def debug(
        self, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log debug message with context."""
        self._log_with_context(logging.DEBUG, message, extra, **kwargs)

    def info(self, message: str, extra: dict[str, Any] | None = None, **kwargs) -> None:
        """Log info message with context."""
        self._log_with_context(logging.INFO, message, extra, **kwargs)

    def warning(
        self, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log warning message with context."""
        self._log_with_context(logging.WARNING, message, extra, **kwargs)

    def error(
        self, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log error message with context."""
        self._log_with_context(logging.ERROR, message, extra, **kwargs)

    def critical(
        self, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log critical message with context."""
        self._log_with_context(logging.CRITICAL, message, extra, **kwargs)

    def exception(
        self, message: str, extra: dict[str, Any] | None = None, **kwargs
    ) -> None:
        """Log exception with context."""
        self._log_with_context(logging.ERROR, message, extra, **kwargs)


__all__ = ["LogContext", "contextual_logger"]
