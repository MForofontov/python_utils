"""
Colored log formatter for console output.

Adds ANSI color codes to log messages based on log level,
making it easier to visually distinguish different types of messages.
"""

import logging
import sys
from typing import Optional


def colored_formatter(fmt: Optional[str] = None, use_color: bool = True) -> logging.Formatter:
    """
    Create a colored log formatter for console output.

    Parameters
    ----------
    fmt : str, optional
        Log format string (default: '%(levelname)s - %(message)s')
    use_color : bool, optional
        Whether to use colors (default True)

    Returns
    -------
    logging.Formatter
        Configured colored formatter

    Examples
    --------
    >>> import logging
    >>> formatter = colored_formatter()
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger = logging.getLogger('test')
    >>> logger.addHandler(handler)
    >>> logger.info('This will be green')
    """

    class ColoredFormatter(logging.Formatter):
        # ANSI color codes
        COLORS = {
            'DEBUG': '\033[36m',      # Cyan
            'INFO': '\033[32m',       # Green
            'WARNING': '\033[33m',    # Yellow
            'ERROR': '\033[31m',      # Red
            'CRITICAL': '\033[35m',   # Magenta
        }

        RESET = '\033[0m'  # Reset to default color

        def __init__(self, fmt: Optional[str] = None, use_color: bool = True):
            if fmt is None:
                fmt = '%(levelname)s - %(message)s'

            super().__init__(fmt)
            self.use_color = use_color and self._supports_color()

        def _supports_color(self) -> bool:
            """Check if terminal supports color output."""
            # Check if output is a TTY and not Windows without color support
            if hasattr(sys.stdout, 'isatty'):
                return sys.stdout.isatty()
            return False

        def format(self, record: logging.LogRecord) -> str:
            # Get the formatted message
            message = super().format(record)

            if self.use_color:
                color = self.COLORS.get(record.levelname, '')
                if color:
                    message = f"{color}{message}{self.RESET}"

            return message

    return ColoredFormatter(fmt, use_color)


__all__ = ['colored_formatter']
