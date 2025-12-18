import pytest
from circuit_breaker_functions.fallback_chain import fallback_chain, FallbackChain


def test_fallback_chain_case_1_normal_operation_first_succeeds() -> None:
    """
    Test case 1: First function succeeds, no fallbacks needed.
    """

    def primary() -> str:
        return "primary"

    def fallback1() -> str:
        return "fallback1"

    result = fallback_chain(primary, fallback1)
    assert result == "primary"


def test_fallback_chain_case_2_second_function_succeeds() -> None:
    """
    Test case 2: First fails, second succeeds.
    """

    def failing() -> str:
        raise ValueError("Failed")

    def success() -> str:
        return "backup"

    result = fallback_chain(failing, success)
    assert result == "backup"


def test_fallback_chain_case_3_multiple_fallbacks() -> None:
    """
    Test case 3: Multiple fallbacks with third succeeding.
    """

    def fail1() -> str:
        raise ValueError("Fail 1")

    def fail2() -> str:
        raise RuntimeError("Fail 2")

    def success() -> str:
        return "third time's the charm"

    result = fallback_chain(fail1, fail2, success)
    assert result == "third time's the charm"


def test_fallback_chain_case_4_with_different_return_types() -> None:
    """
    Test case 4: Functions with different but compatible return types.
    """

    def get_int() -> int:
        raise ValueError("No int")

    def get_float() -> float:
        return 3.14

    result = fallback_chain(get_int, get_float)
    assert result == 3.14


def test_fallback_chain_case_5_edge_case_all_functions_fail() -> None:
    """
    Test case 5: All functions fail, last exception is raised.
    """

    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Error 2")

    def fail3() -> str:
        raise TypeError("Error 3")

    with pytest.raises(TypeError, match="Error 3"):
        fallback_chain(fail1, fail2, fail3)


def test_fallback_chain_case_6_edge_case_single_function() -> None:
    """
    Test case 6: Single function in chain.
    """

    def only_func() -> str:
        return "only one"

    result = fallback_chain(only_func)
    assert result == "only one"


def test_fallback_chain_case_7_edge_case_single_function_fails() -> None:
    """
    Test case 7: Single function fails.
    """

    def failing() -> str:
        raise ValueError("Failed")

    with pytest.raises(ValueError, match="Failed"):
        fallback_chain(failing)


def test_fallback_chain_case_8_value_error_no_functions() -> None:
    """
    Test case 8: ValueError when no functions provided.
    """
    with pytest.raises(ValueError, match="At least one function must be provided"):
        fallback_chain()


def test_fallback_chain_case_9_type_error_non_callable() -> None:
    """
    Test case 9: TypeError when non-callable is provided.
    """

    def valid_func() -> str:
        return "valid"

    with pytest.raises(TypeError, match="All arguments must be callable"):
        fallback_chain(valid_func, "not_callable")  # type: ignore[arg-type]


def test_fallback_chain_class_case_1_normal_operation() -> None:
    """
    Test case 10: FallbackChain class normal operation.
    """
    chain = FallbackChain()

    def primary() -> str:
        return "primary result"

    chain.add(primary)

    result = chain.execute()
    assert result == "primary result"


def test_fallback_chain_class_case_2_multiple_handlers() -> None:
    """
    Test case 11: FallbackChain with multiple handlers.
    """
    chain = FallbackChain()

    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Error 2")

    def success() -> str:
        return "success"

    chain.add(fail1)
    chain.add(fail2)
    chain.add(success)

    result = chain.execute()
    assert result == "success"


def test_fallback_chain_class_case_3_with_args() -> None:
    """
    Test case 12: FallbackChain execute with arguments.
    """
    chain = FallbackChain()

    def add_numbers(a: int, b: int) -> int:
        return a + b

    chain.add(add_numbers)

    result = chain.execute(3, 5)
    assert result == 8


def test_fallback_chain_class_case_4_with_kwargs() -> None:
    """
    Test case 13: FallbackChain execute with keyword arguments.
    """
    chain = FallbackChain()

    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    chain.add(greet)

    result = chain.execute(name="World", greeting="Hi")
    assert result == "Hi, World!"


def test_fallback_chain_class_case_5_clear_handlers() -> None:
    """
    Test case 14: Clear all handlers from chain.
    """
    chain = FallbackChain()

    def func() -> str:
        return "test"

    chain.add(func)
    assert len(chain.handlers) == 1

    chain.clear()
    assert len(chain.handlers) == 0


def test_fallback_chain_class_case_6_edge_case_first_succeeds() -> None:
    """
    Test case 15: First handler succeeds, others not called.
    """
    chain = FallbackChain()
    call_count = {"primary": 0, "fallback": 0}

    def primary() -> str:
        call_count["primary"] += 1
        return "primary"

    def fallback() -> str:
        call_count["fallback"] += 1
        return "fallback"

    chain.add(primary)
    chain.add(fallback)

    result = chain.execute()
    assert result == "primary"
    assert call_count["primary"] == 1
    assert call_count["fallback"] == 0  # Should not be called


def test_fallback_chain_class_case_7_edge_case_all_fail() -> None:
    """
    Test case 16: All handlers fail, last exception raised.
    """
    chain = FallbackChain()

    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Final error")

    chain.add(fail1)
    chain.add(fail2)

    with pytest.raises(RuntimeError, match="Final error"):
        chain.execute()


def test_fallback_chain_class_case_8_edge_case_empty_chain() -> None:
    """
    Test case 17: Execute on empty chain.
    """
    chain = FallbackChain()

    with pytest.raises(RuntimeError, match="No handlers in fallback chain"):
        chain.execute()


def test_fallback_chain_class_case_9_add_multiple_at_once() -> None:
    """
    Test case 18: Add multiple handlers sequentially.
    """
    chain = FallbackChain()

    def func1() -> str:
        raise ValueError("Fail")

    def func2() -> str:
        return "success"

    chain.add(func1)
    chain.add(func2)

    assert len(chain.handlers) == 2

    result = chain.execute()
    assert result == "success"


def test_fallback_chain_class_case_10_handler_order_preserved() -> None:
    """
    Test case 19: Handlers executed in order added.
    """
    chain = FallbackChain()
    execution_order = []

    def first() -> str:
        execution_order.append(1)
        raise ValueError("First fails")

    def second() -> str:
        execution_order.append(2)
        raise RuntimeError("Second fails")

    def third() -> str:
        execution_order.append(3)
        return "success"

    chain.add(first)
    chain.add(second)
    chain.add(third)

    result = chain.execute()

    assert result == "success"
    assert execution_order == [1, 2, 3]


def test_fallback_chain_class_case_11_type_error_non_callable() -> None:
    """
    Test case 20: TypeError when adding non-callable to chain.
    """
    chain = FallbackChain()

    with pytest.raises(TypeError, match="handler must be callable"):
        chain.add("not_callable")  # type: ignore[arg-type]


def test_fallback_chain_class_case_12_type_error_add_none() -> None:
    """
    Test case 21: TypeError when adding None to chain.
    """
    chain = FallbackChain()

    with pytest.raises(TypeError, match="handler must be callable"):
        chain.add(None)  # type: ignore[arg-type]
