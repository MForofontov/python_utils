def print_message(message: str, message_type: str = "info", end = '\n', flush: bool = False) -> None:
    """
    Print a formatted message with the current time and message type.

    Parameters
    ----------
    message : str
        The message to print.
    message_type : str
        The type of message (e.g., "info", "warning", "error").
    logger : bool
        Whether to log the message.

    Returns
    -------
    None
    """
    logger: Optional[logging.Logger] = gb.LOGGER # This can change to a logger object if user uses --logger

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
    # Log the message if logger is not None
    if logger:
        if message_type == "info":
            logger.info(message)
        elif message_type == "warning":
            logger.warning(message)
        elif message_type == "error":
            logger.error(message)
        elif message_type == "debug":
            logger.debug(message)
        else:
            logger.info(message)
    
    print(formatted_message, end = end, flush = flush)
