import pytest
import logging
from typing import Any
from decorators.event_trigger import event_trigger, EventManager

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


def test_event_trigger_basic() -> None:
    """
    Test case 1: Basic functionality of event_trigger
    """
    # Example event manager
    event_manager = EventManager()

    # Example function to be decorated
    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function(a: int, b: str) -> str:
        return f"{a} - {b}"

    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)
    result = sample_function(1, "test")
    assert result == "1 - test"
    assert triggered == [(1, "test")]


def test_event_trigger_with_kwargs() -> None:
    """
    Test case 2: Event trigger with kwargs
    """
    # Example event manager
    event_manager = EventManager()

    # Example function to be decorated
    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function(a: int, b: str) -> str:
        return f"{a} - {b}"

    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)

    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function_kwargs(a: int, b: str) -> str:
        return f"{a} - {b}"

    result = sample_function_kwargs(a=1, b="test")
    assert result == "1 - test"
    assert triggered == [(1, "test")]


def test_event_trigger_with_mixed_args() -> None:
    """
    Test case 3: Event trigger with mixed args and kwargs
    """
    # Example event manager
    event_manager = EventManager()
    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)

    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function_mixed(a: int, b: str, c: int) -> str:
        return f"{a} - {b} - {c}"

    result = sample_function_mixed(1, b="test", c=2)
    assert result == "1 - test - 2"
    assert triggered == [(1, {"b": "test", "c": 2})]


def test_event_trigger_with_variable_length_arguments() -> None:
    """
    Test case 4: Event trigger with variable length arguments (*args and **kwargs)
    """
    # Example event manager
    event_manager = EventManager()

    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
        return f"args: {args}, kwargs: {kwargs}"

    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)
    result = sample_function_args_kwargs(1, 2, 3, kwarg1="test", kwarg2="example")
    assert result == "args: (1, 2, 3), kwargs: {'kwarg1': 'test', 'kwarg2': 'example'}"
    assert triggered == [((1, 2, 3), {"kwarg1": "test", "kwarg2": "example"})]


def test_event_trigger_mixed_type_arguments() -> None:
    """
    Test case 5: Event trigger with mixed type arguments
    """
    # Example event manager
    event_manager = EventManager()

    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)

    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function_mixed_types(a: int, b: str, c: float) -> str:
        return f"{a} - {b} - {c}"

    result = sample_function_mixed_types(1, "test", 2.0)
    assert result == "1 - test - 2.0"
    assert triggered == [(1, "test", 2.0)]


def test_event_trigger_function_raises_error(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 6: Event trigger when the wrapped function raises an error
    """
    # Example event manager
    event_manager = EventManager()

    triggered = []

    def handler(*args: Any, **kwargs: Any) -> None:
        triggered.append((args, kwargs))

    event_manager.subscribe("test_event", handler)

    @event_trigger(event_manager, "test_event", logger=test_logger)
    def sample_function_raises_error(a: int, b: str) -> str:
        raise ValueError("An error occurred")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="An error occurred"):
            sample_function_raises_error(1, "test")
    assert "An error occurred" in caplog.text
    # The event should still be triggered if the function raises an error
    assert triggered == [(1, "test")]


def test_event_trigger_invalid_logger() -> None:
    """
    Test case 7: Invalid logger type
    """
    # Example event manager
    event_manager = EventManager()

    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @event_trigger(event_manager, "test_event", logger="invalid_logger")
        def sample_function_invalid_logger(a: int, b: str) -> str:
            return f"{a} - {b}"


def test_event_trigger_invalid_event_manager() -> None:
    """
    Test case 8: Invalid event manager type
    """
    with pytest.raises(
        TypeError, match="event_manager must be an instance of EventManager"
    ):

        @event_trigger("invalid_event_manager", "test_event", logger=test_logger)
        def sample_function_invalid_event_manager(a: int, b: str) -> str:
            return f"{a} - {b}"


def test_event_trigger_invalid_event_name() -> None:
    """
    Test case 9: Invalid event name type
    """
    # Example event manager
    event_manager = EventManager()

    with pytest.raises(TypeError, match="event_name must be a non-empty string"):

        @event_trigger(event_manager, 123, logger=test_logger)
        def sample_function_invalid_event_name(a: int, b: str) -> str:
            return f"{a} - {b}"
