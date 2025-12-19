import pytest
from testing_functions.assertion_helpers.assert_raises_with_message import (
    assert_raises_with_message,
)


def test_assert_raises_with_message_correct_exception_and_message() -> None:
    """
    Test case 1: Assert correct exception and message.
    """
    # Arrange
    def failing_func():
        raise ValueError("Invalid input")
    
    # Act & Assert
    assert_raises_with_message(failing_func, ValueError, "Invalid")


def test_assert_raises_with_message_full_message_match() -> None:
    """
    Test case 2: Assert with full message match.
    """
    # Arrange
    def failing_func():
        raise TypeError("Expected int, got str")
    
    # Act & Assert
    assert_raises_with_message(failing_func, TypeError, "Expected int, got str")


def test_assert_raises_with_message_with_args() -> None:
    """
    Test case 3: Assert exception with function args.
    """
    # Arrange
    def failing_func(x, y):
        raise ValueError(f"Sum {x+y} is invalid")
    
    # Act & Assert
    assert_raises_with_message(failing_func, ValueError, "Sum", 1, 2)


def test_assert_raises_with_message_with_kwargs() -> None:
    """
    Test case 4: Assert exception with function kwargs.
    """
    # Arrange
    def failing_func(value=None):
        raise RuntimeError(f"Value {value} not allowed")
    
    # Act & Assert
    assert_raises_with_message(failing_func, RuntimeError, "not allowed", value=42)


def test_assert_raises_with_message_type_error_func() -> None:
    """
    Test case 5: TypeError for non-callable func.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="func must be callable"):
        assert_raises_with_message("not callable", ValueError, "message")


def test_assert_raises_with_message_type_error_exception_type() -> None:
    """
    Test case 6: TypeError for invalid exception_type.
    """
    # Arrange
    def dummy_func():
        pass
    
    # Act & Assert
    with pytest.raises(TypeError, match="exception_type must be an Exception type"):
        assert_raises_with_message(dummy_func, "ValueError", "message")


def test_assert_raises_with_message_type_error_message_pattern() -> None:
    """
    Test case 7: TypeError for invalid message_pattern type.
    """
    # Arrange
    def dummy_func():
        raise ValueError("test")
    
    # Act & Assert
    with pytest.raises(TypeError, match="message_pattern must be a string"):
        assert_raises_with_message(dummy_func, ValueError, 123)


def test_assert_raises_with_message_assertion_error_no_exception() -> None:
    """
    Test case 8: AssertionError when no exception raised.
    """
    # Arrange
    def passing_func():
        return 42
    
    # Act & Assert
    with pytest.raises(AssertionError, match="Expected .* to be raised, but no exception was raised"):
        assert_raises_with_message(passing_func, ValueError, "message")


def test_assert_raises_with_message_assertion_error_wrong_exception() -> None:
    """
    Test case 9: AssertionError when wrong exception type raised.
    """
    # Arrange
    def failing_func():
        raise TypeError("type error")
    
    # Act & Assert
    with pytest.raises(AssertionError, match="Expected .* but got"):
        assert_raises_with_message(failing_func, ValueError, "message")


def test_assert_raises_with_message_assertion_error_message_mismatch() -> None:
    """
    Test case 10: AssertionError when message doesn't match.
    """
    # Arrange
    def failing_func():
        raise ValueError("wrong message")
    
    # Act & Assert
    with pytest.raises(AssertionError, match="does not contain expected pattern"):
        assert_raises_with_message(failing_func, ValueError, "correct")
