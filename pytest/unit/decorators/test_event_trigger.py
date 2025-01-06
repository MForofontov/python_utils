import pytest
import logging
from decorators.event_trigger import EventManager, event_trigger

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

# Initialize the EventManager
event_manager = EventManager()

# Example callback functions
def callback_one(*args, **kwargs):
    callback_one.called = True
    callback_one.args = args
    callback_one.kwargs = kwargs

def callback_two(*args, **kwargs):
    callback_two.called = True
    callback_two.args = args
    callback_two.kwargs = kwargs

# Reset callback state
def reset_callbacks():
    callback_one.called = False
    callback_one.args = None
    callback_one.kwargs = None
    callback_two.called = False
    callback_two.args = None
    callback_two.kwargs = None

# Subscribe callbacks to events
event_manager.subscribe("event_one", callback_one)
event_manager.subscribe("event_two", callback_one)
event_manager.subscribe("event_two", callback_two)

@event_trigger(event_manager, "event_one")
def example_function_one(a, b):
    return f"Result: {a + b}"

@event_trigger(event_manager, "event_two")
def example_function_two(a, b):
    return f"Result: {a * b}"

def test_event_trigger_single_callback():
    """
    Test case 1: Single callback triggered
    """
    # Test case 1: Single callback triggered
    reset_callbacks()
    result = example_function_one(1, 2)
    assert result == "Result: 3"
    assert callback_one.called
    assert callback_one.args == (1, 2)
    assert callback_one.kwargs == {}

def test_event_trigger_multiple_callbacks():
    """
    Test case 2: Multiple callbacks triggered
    """
    # Test case 2: Multiple callbacks triggered
    reset_callbacks()
    result = example_function_two(2, 3)
    assert result == "Result: 6"
    assert callback_two.called
    assert callback_two.args == (2, 3)
    assert callback_two.kwargs == {}
    assert callback_one.called
    assert callback_one.args == (2, 3)
    assert callback_one.kwargs == {}

def test_event_trigger_with_args_and_kwargs():
    """
    Test case 3: Callbacks with arguments and keyword arguments
    """
    # Test case 3: Callbacks with arguments and keyword arguments
    reset_callbacks()
    event_manager.trigger("event_one", 1, 2, key="value")
    assert callback_one.called
    assert callback_one.args == (1, 2)
    assert callback_one.kwargs == {"key": "value"}

def test_event_trigger_invalid_event():
    """
    Test case 4: Triggering an invalid event
    """
    # Test case 4: Triggering an invalid event
    reset_callbacks()
    event_manager.trigger("invalid_event")
    assert not callback_one.called
    assert not callback_two.called

def test_event_trigger_invalid_event_manager():
    """
    Test case 5: Invalid event manager type, no logger provided
    """
    # Test case 5: Invalid event manager type, no logger provided
    with pytest.raises(TypeError, match="event_manager be a non-empty instance of EventManager"):
        @event_trigger("invalid_event_manager", "event_one")
        def example_function_invalid_event_manager(a, b):
            return f"Result: {a + b}"

def test_event_trigger_invalid_event_name_type():
    """
    Test case 6: Invalid event name type, no logger provided
    """
    # Test case 6: Invalid event name type, no logger provided
    with pytest.raises(TypeError, match="event_name must be a non-empty string"):
        @event_trigger(event_manager, 123)
        def example_function_invalid_event_name_type(a, b):
            return f"Result: {a + b}"

def test_event_trigger_invalid_logger():
    """
    Test case 7: Invalid logger (not an instance of logging.Logger or None)
    """
    # Test case 7: Invalid logger (not an instance of logging.Logger or None)
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @event_trigger(event_manager, "event_one", logger="not_a_logger")
        def example_function_invalid_logger(a, b):
            return f"Result: {a + b}"

def test_event_trigger_invalid_event_manager_logger(caplog):
    """
    Test case 8: Invalid event manager type, with logger provided
    """
    # Test case 8: Invalid event manager type, with logger provided
    with caplog.at_level(logging.ERROR):
        @event_trigger("invalid_event_manager", "event_one")
        def example_function_invalid_event_manager(a, b):
            return f"Result: {a + b}"
    assert "event_manager be a non-empty instance of EventManager" in caplog.text

def test_event_trigger_invalid_event_name_type_logger(caplog):
    """
    Test case 9: Invalid event name type, with logger provided
    """
    # Test case 9: Invalid event name type, with logger provided
    with caplog.at_level(logging.ERROR):
        @event_trigger(event_manager, 123)
        def example_function_invalid_event_name_type(a, b):
            return f"Result: {a + b}"
    assert "event_name must be a non-empty string" in caplog.text
