import pytest
from circuit_breaker_functions.fallback_chain import fallback_chain, FallbackChain


def test_fallback_chain_normal_operation_first_succeeds() -> None:
    """
    Test case 1: First function succeeds, no fallbacks needed.
    """

    def primary() -> str:
        return "primary"

    def fallback1() -> str:
        return "fallback1"

    result = fallback_chain(primary, [fallback1])
    assert result == "primary"


def test_fallback_chain_second_function_succeeds() -> None:
    """
    Test case 2: First fails, second succeeds.
    """

    def failing() -> str:
        raise ValueError("Failed")

    def success() -> str:
        return "backup"

    result = fallback_chain(failing, [success])
    assert result == "backup"


def test_fallback_chain_multiple_fallbacks() -> None:
    """
    Test case 3: Multiple fallbacks with third succeeding.
    """

    def fail1() -> str:
        raise ValueError("Fail 1")

    def fail2() -> str:
        raise RuntimeError("Fail 2")

    def success() -> str:
        return "third time's the charm"

    result = fallback_chain(fail1, [fail2, success])
    assert result == "third time's the charm"


def test_fallback_chain_with_different_return_types() -> None:
    """
    Test case 4: Functions with different but compatible return types.
    """

    def get_int() -> int:
        raise ValueError("No int")

    def get_float() -> float:
        return 3.14

    result = fallback_chain(get_int, [get_float])
    assert result == 3.14


def test_fallback_chain_edge_case_all_functions_fail() -> None:
    """
    Test case 5: All functions fail, last exception is raised.
    """

    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Error 2")

    def fail3() -> str:
        raise TypeError("Error 3")

    with pytest.raises(Exception, match="Error 3"):
        fallback_chain(fail1, [fail2, fail3])


def test_fallback_chain_edge_case_empty_fallbacks_list() -> None:
    """
    Test case 6: Empty fallbacks list raises ValueError.
    """

    def only_func() -> str:
        return "only one"

    with pytest.raises(ValueError, match="fallbacks list cannot be empty"):
        fallback_chain(only_func, [])


def test_fallback_chain_edge_case_all_fail() -> None:
    """
    Test case 7: All functions fail raises exception.
    """

    def failing() -> str:
        raise ValueError("Failed")

    def failing2() -> str:
        raise ValueError("Also failed")

    with pytest.raises(Exception, match="All functions in fallback chain failed"):
        fallback_chain(failing, [failing2])


def test_fallback_chain_type_error_primary_not_callable() -> None:
    """
    Test case 8: TypeError when primary is not callable.
    """
    with pytest.raises(TypeError, match="primary must be callable"):
        fallback_chain("not_callable", [lambda: "test"])  # type: ignore[arg-type]


def test_fallback_chain_type_error_non_callable() -> None:
    """
    Test case 9: TypeError when non-callable is provided.
    """

    def valid_func() -> str:
        return "valid"

    with pytest.raises(TypeError, match="fallbacks must be a list"):
        fallback_chain(valid_func, "not_callable")  # type: ignore[arg-type]


def test_fallback_chain_class_normal_operation() -> None:
    """
    Test case 10: FallbackChain class normal operation.
    """
    def primary() -> str:
        return "primary result"

    def fallback() -> str:
        return "fallback"

    chain = FallbackChain(primary, [fallback])

    result = chain.execute()
    assert result == "primary result"


def test_fallback_chain_class_multiple_handlers() -> None:
    """
    Test case 11: FallbackChain with multiple handlers.
    """
    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Error 2")

    def success() -> str:
        return "success"

    chain = FallbackChain(fail1, [fail2, success])

    result = chain.execute()
    assert result == "success"


def test_fallback_chain_class_with_args() -> None:
    """
    Test case 12: FallbackChain execute with arguments.
    """
    def add_numbers(a: int, b: int) -> int:
        return a + b

    def fallback(a: int, b: int) -> int:
        return 0

    chain = FallbackChain(add_numbers, [fallback])

    result = chain.execute(3, 5)
    assert result == 8


def test_fallback_chain_class_with_kwargs() -> None:
    """
    Test case 13: FallbackChain execute with keyword arguments.
    """
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    def fallback_greet(name: str, greeting: str = "Hello") -> str:
        return "default"

    chain = FallbackChain(greet, [fallback_greet])

    result = chain.execute(name="World", greeting="Hi")
    assert result == "Hi, World!"


def test_fallback_chain_class_add_fallback() -> None:
    """
    Test case 14: Add additional fallback to chain.
    """
    def primary() -> str:
        return "test"

    def fallback1() -> str:
        return "fallback1"

    def fallback2() -> str:
        return "fallback2"

    chain = FallbackChain(primary, [fallback1])
    assert len(chain.fallbacks) == 1

    chain.add_fallback(fallback2)
    assert len(chain.fallbacks) == 2


def test_fallback_chain_class_edge_case_first_succeeds() -> None:
    """
    Test case 15: First handler succeeds, others not called.
    """
    call_count = {"primary": 0, "fallback": 0}

    def primary() -> str:
        call_count["primary"] += 1
        return "primary"

    def fallback() -> str:
        call_count["fallback"] += 1
        return "fallback"

    chain = FallbackChain(primary, [fallback])

    result = chain.execute()
    assert result == "primary"
    assert call_count["primary"] == 1
    assert call_count["fallback"] == 0  # Should not be called


def test_fallback_chain_class_edge_case_all_fail() -> None:
    """
    Test case 16: All handlers fail, exception raised.
    """
    def fail1() -> str:
        raise ValueError("Error 1")

    def fail2() -> str:
        raise RuntimeError("Final error")

    chain = FallbackChain(fail1, [fail2])

    with pytest.raises(Exception, match="All functions in fallback chain failed"):
        chain.execute()


def test_fallback_chain_class_edge_case_empty_fallbacks() -> None:
    """
    Test case 17: Cannot create chain with empty fallbacks list.
    """
    def primary() -> str:
        return "test"

    with pytest.raises(ValueError, match="fallbacks list cannot be empty"):
        FallbackChain(primary, [])


def test_fallback_chain_class_add_multiple_fallbacks() -> None:
    """
    Test case 18: Add multiple fallbacks to chain.
    """
    def primary() -> str:
        raise ValueError("Fail")

    def fallback1() -> str:
        raise ValueError("Also fail")

    def fallback2() -> str:
        return "success"

    chain = FallbackChain(primary, [fallback1])
    assert len(chain.fallbacks) == 1

    chain.add_fallback(fallback2)
    assert len(chain.fallbacks) == 2

    result = chain.execute()
    assert result == "success"


def test_fallback_chain_class_fallback_order_preserved() -> None:
    """
    Test case 19: Fallbacks executed in order.
    """
    execution_order = []

    def primary() -> str:
        execution_order.append(1)
        raise ValueError("First fails")

    def second() -> str:
        execution_order.append(2)
        raise RuntimeError("Second fails")

    def third() -> str:
        execution_order.append(3)
        return "success"

    chain = FallbackChain(primary, [second, third])

    result = chain.execute()

    assert result == "success"
    assert execution_order == [1, 2, 3]


def test_fallback_chain_class_type_error_non_callable_fallback() -> None:
    """
    Test case 20: TypeError when adding non-callable fallback.
    """
    def primary() -> str:
        return "test"

    def fallback() -> str:
        return "fallback"

    chain = FallbackChain(primary, [fallback])

    with pytest.raises(TypeError, match="fallback must be callable"):
        chain.add_fallback("not_callable")  # type: ignore[arg-type]


def test_fallback_chain_class_type_error_non_callable_primary() -> None:
    """
    Test case 21: TypeError when primary is not callable.
    """
    def fallback() -> str:
        return "fallback"

    with pytest.raises(TypeError, match="primary must be callable"):
        FallbackChain("not_callable", [fallback])  # type: ignore[arg-type]
