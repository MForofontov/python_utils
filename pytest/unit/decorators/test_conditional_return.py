import pytest
from decorators.conditional_return import conditional_return

# Example condition functions
def always_true():
    return True

def always_false():
    return False

def condition_based_on_args(a, b):
    return a > b

def condition_based_on_kwargs(**kwargs):
    return kwargs.get('flag', False)

def condition_based_on_mixed_args(a, b, **kwargs):
    return a > b and kwargs.get('flag', False)

def condition_no_args():
    return True

def condition_raises_exception(*args, **kwargs):
    raise ValueError("Condition raised an exception")

# Example functions to be decorated
@conditional_return(always_true, "Condition met")
def example_function_true(a, b):
    return f"Result: {a + b}"

@conditional_return(always_false, "Condition met")
def example_function_false(a, b):
    return f"Result: {a + b}"

@conditional_return(condition_based_on_args, "Condition met")
def example_function_conditional(a, b):
    return f"Result: {a + b}"

@conditional_return(condition_based_on_kwargs, "Condition met")
def example_function_kwargs(a, b, **kwargs):
    return f"Result: {a + b}"

@conditional_return(condition_based_on_mixed_args, "Condition met")
def example_function_mixed_args(a, b, **kwargs):
    return f"Result: {a + b}"

@conditional_return(condition_no_args, "Condition met")
def example_function_no_args(a, b):
    return f"Result: {a + b}"

@conditional_return(condition_raises_exception, "Condition met")
def example_function_raises_exception(a, b):
    return f"Result: {a + b}"

def test_conditional_return_always_true():
    """
    Test case 1: Condition always true
    """
    # Test case 1: Condition always true
    result = example_function_true(1, 2)
    assert result == "Condition met"

def test_conditional_return_always_false():
    """
    Test case 2: Condition always false
    """
    # Test case 2: Condition always false
    result = example_function_false(1, 2)
    assert result == "Result: 3"

def test_conditional_return_condition_met():
    """
    Test case 3: Condition met based on arguments
    """
    # Test case 3: Condition met based on arguments
    result = example_function_conditional(3, 2)
    assert result == "Condition met"

def test_conditional_return_condition_not_met():
    """
    Test case 4: Condition not met based on arguments
    """
    # Test case 4: Condition not met based on arguments
    result = example_function_conditional(1, 2)
    assert result == "Result: 3"

def test_conditional_return_condition_met_kwargs():
    """
    Test case 5: Condition met based on keyword arguments
    """
    # Test case 5: Condition met based on keyword arguments
    result = example_function_kwargs(1, 2, flag=True)
    assert result == "Condition met"

def test_conditional_return_condition_not_met_kwargs():
    """
    Test case 6: Condition not met based on keyword arguments
    """
    # Test case 6: Condition not met based on keyword arguments
    result = example_function_kwargs(1, 2, flag=False)
    assert result == "Result: 3"

def test_conditional_return_condition_met_mixed_args():
    """
    Test case 7: Condition met based on mixed arguments and keyword arguments
    """
    # Test case 7: Condition met based on mixed arguments and keyword arguments
    result = example_function_mixed_args(3, 2, flag=True)
    assert result == "Condition met"

def test_conditional_return_condition_not_met_mixed_args():
    """
    Test case 8: Condition not met based on mixed arguments and keyword arguments
    """
    # Test case 8: Condition not met based on mixed arguments and keyword arguments
    result = example_function_mixed_args(1, 2, flag=True)
    assert result == "Result: 3"

def test_conditional_return_no_args():
    """
    Test case 9: Condition with no arguments
    """
    # Test case 9: Condition with no arguments
    result = example_function_no_args(1, 2)
    assert result == "Condition met"

def test_conditional_return_with_default_args():
    """
    Test case 10: Function with default arguments
    """
    # Test case 10: Function with default arguments
    @conditional_return(lambda a, b=0: a > b, "Condition met")
    def example_function_default_args(a, b=0):
        return f"Result: {a + b}"
    
    result = example_function_default_args(3)
    assert result == "Condition met"
    
    result = example_function_default_args(1, 2)
    assert result == "Result: 3"

def test_conditional_return_function_no_args():
    """
    Test case 11: Function with no arguments
    """
    # Test case 11: Function with no arguments
    @conditional_return(always_true, "Condition met")
    def example_function_no_args():
        return "Original result"
    
    result = example_function_no_args()
    assert result == "Condition met"

def test_conditional_return_condition_raises_exception():
    """
    Test case 12: Condition raises an exception
    """
    # Test case 12: Condition raises an exception
    with pytest.raises(RuntimeError, match="Condition function raised an error: Condition raised an exception"):
        example_function_raises_exception(1, 2)

def test_conditional_return_invalid_condition():
    """
    Test case 13: Invalid condition (not callable)
    """
    # Test case 13: Invalid condition (not callable)
    with pytest.raises(TypeError, match="Condition must be callable"):
        @conditional_return("not a callable", "Condition met")
        def example_function_invalid(a, b):
            return f"Result: {a + b}"
