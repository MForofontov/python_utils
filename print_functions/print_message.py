import logging
from datetime import datetime
from typing import Optional
try:
    from logger_functions.logger import logger
except ModuleNotFoundError:  # pragma: no cover - fallback for standalone execution
    logger = logging.getLogger(__name__)

def print_message(message: str, message_type: str = "info", end: str = '\n', flush: bool = False) -> None:
    """
    Print a formatted message with the current time and message type.

    Parameters
    ----------
    message : str
        The message to print.
    message_type : str
        The type of message (e.g., "info", "warning", "error").
    end : str
        The end character to use in the print function.
    flush : bool
        Whether to flush the print buffer.


    Returns
    -------
    None

    Notes
    -----
    Messages are logged through the :data:`logger` object imported from
    ``logger_functions.logger``.
    """
    logger_to_use: Optional[logging.Logger] = logger # This can change to a logger object if user uses --logger

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message_type == "info":
        formatted_message = f"[INFO] {current_time} - {message}"
    elif message_type == "warning":
        formatted_message = f"[WARNING] {current_time} - {message}"
    elif message_type == "error":
        formatted_message = f"[ERROR] {current_time} - {message}"
    elif message_type == "debug":
        formatted_message = f"[DEBUG] {current_time} - {message}"
    elif message_type == None:
        formatted_message = f"{message}"
    else:
        formatted_message = f"{current_time} - {message}"
    # Log the message if logger_to_use is not None
    if logger_to_use:
        if message_type == "info":
            logger_to_use.info(message)
        elif message_type == "warning":
            logger_to_use.warning(message)
        elif message_type == "error":
            logger_to_use.error(message)
        elif message_type == "debug":
            logger_to_use.debug(message)
        else:
            logger_to_use.info(message)
    
    print(formatted_message, end = end, flush = flush)
