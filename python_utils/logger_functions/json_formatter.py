"""JSON log formatter for structured logging."""

import json
import logging
from datetime import datetime


def json_formatter(
    include_extra: bool = True, pretty_print: bool = False
) -> logging.Formatter:
    """
    Create a JSON log formatter for structured logging.

    Parameters
    ----------
    include_extra : bool, optional
        Whether to include extra fields from the log record (default True)
    pretty_print : bool, optional
        Whether to pretty-print JSON output (default False)

    Returns
    -------
    logging.Formatter
        Configured JSON formatter

    Examples
    --------
    >>> import logging
    >>> formatter = json_formatter()
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger = logging.getLogger('test')
    >>> logger.addHandler(handler)
    >>> logger.info('Test message')
    {"timestamp": "2024-01-01T12:00:00", "level": "INFO", ...}
    """

    class JsonFormatter(logging.Formatter):
        def __init__(self, include_extra: bool = True, pretty_print: bool = False):
            super().__init__()
            self.include_extra = include_extra
            self.pretty_print = pretty_print

        def format(self, record: logging.LogRecord) -> str:
            # Create base log entry
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "process": record.process,
                "thread": record.thread,
            }

            # Add exception info if present
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)

            # Add extra fields if requested
            if self.include_extra:
                for key, value in record.__dict__.items():
                    if key not in {
                        "name",
                        "msg",
                        "args",
                        "levelname",
                        "levelno",
                        "pathname",
                        "filename",
                        "module",
                        "exc_info",
                        "exc_text",
                        "stack_info",
                        "lineno",
                        "funcName",
                        "created",
                        "msecs",
                        "relativeCreated",
                        "thread",
                        "threadName",
                        "processName",
                        "process",
                        "message",
                    }:
                        log_entry[key] = value

            # Format as JSON
            if self.pretty_print:
                return json.dumps(log_entry, indent=2, default=str)
            else:
                return json.dumps(log_entry, default=str)

    return JsonFormatter(include_extra, pretty_print)


__all__ = ["json_formatter"]
