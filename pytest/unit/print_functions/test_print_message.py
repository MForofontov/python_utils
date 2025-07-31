import logging
from print_functions.print_message import print_message

# Create a dedicated logger for tests
custom_logger = logging.getLogger("test_print_message_logger")
custom_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s:%(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)


def test_print_message_uses_module_logger(caplog) -> None:
    """Test logging with the default module logger."""
    with caplog.at_level(logging.INFO):
        print_message("hello world", "info")
        assert "hello world" in caplog.text


def test_print_message_uses_provided_logger(caplog) -> None:
    """Test logging when a custom logger is supplied."""
    with caplog.at_level(logging.WARNING):
        print_message("custom warning", "warning", logger=custom_logger)
        assert "custom warning" in caplog.text
