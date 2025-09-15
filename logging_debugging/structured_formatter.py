"""
Structured log formatter with consistent field alignment.

Formats logs with aligned fields for better readability in console output.
"""

import logging
from datetime import datetime


def structured_formatter(
    max_level_width: int = 8, max_module_width: int = 15
) -> logging.Formatter:
    """
    Create a structured log formatter with consistent field alignment.

    Parameters
    ----------
    max_level_width : int, optional
        Maximum width for level name field (default 8)
    max_module_width : int, optional
        Maximum width for module name field (default 15)

    Returns
    -------
    logging.Formatter
        Configured structured formatter

    Examples
    --------
    >>> import logging
    >>> formatter = structured_formatter()
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger = logging.getLogger('test')
    >>> logger.addHandler(handler)
    >>> logger.info('Structured message')
    2024-01-01 12:00:00 | INFO     | test     | <module>:1 | Structured message
    """

    class StructuredFormatter(logging.Formatter):
        def __init__(self, max_level_width: int = 8, max_module_width: int = 15):
            super().__init__()
            self.max_level_width = max_level_width
            self.max_module_width = max_module_width

        def format(self, record: logging.LogRecord) -> str:
            # Format timestamp
            timestamp = datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Format level with padding
            level = f"{record.levelname:<{self.max_level_width}}"

            # Format module with padding
            module = f"{record.module:<{self.max_module_width}}"

            # Format function and line
            location = f"{record.funcName}:{record.lineno}"

            # Combine all parts
            formatted = (
                f"{timestamp} | {level} | {module} | {location} | {record.getMessage()}"
            )

            return formatted

    return StructuredFormatter(max_level_width, max_module_width)


__all__ = ["structured_formatter"]
