"""
Performance-focused log formatter.

Includes timing information and performance metrics in log output.
"""

import logging
import time
from datetime import datetime


def performance_formatter(include_thread_info: bool = True) -> logging.Formatter:
    """
    Create a performance-focused log formatter.

    Parameters
    ----------
    include_thread_info : bool, optional
        Whether to include thread information (default True)

    Returns
    -------
    logging.Formatter
        Configured performance formatter

    Examples
    --------
    >>> import logging
    >>> formatter = performance_formatter()
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger = logging.getLogger('test')
    >>> logger.addHandler(handler)
    >>> logger.info('Performance message')
    [12:00:00.123] | T12345 | INFO | test.<module>:1 | +0.0ms | Performance message
    """

    class PerformanceFormatter(logging.Formatter):
        def __init__(self, include_thread_info: bool = True):
            super().__init__()
            self.include_thread_info = include_thread_info
            self.start_time = time.perf_counter()

        def format(self, record: logging.LogRecord) -> str:
            # Calculate elapsed time since start
            elapsed_ms = (time.perf_counter() - self.start_time) * 1000
            if elapsed_ms < 1.0:
                elapsed_ms = 0.0

            # Format timestamp with milliseconds
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")[
                :-3
            ]

            # Build performance info
            perf_parts = [f"[{timestamp}]"]

            if self.include_thread_info:
                perf_parts.append(f"T{record.thread}")

            perf_parts.extend(
                [
                    f"{record.levelname}",
                    f"{record.module}.{record.funcName}:{record.lineno}",
                    f"+{elapsed_ms:.1f}ms",
                ]
            )

            # Add message
            perf_parts.append(record.getMessage())

            return " | ".join(perf_parts)

    return PerformanceFormatter(include_thread_info)


__all__ = ["performance_formatter"]
