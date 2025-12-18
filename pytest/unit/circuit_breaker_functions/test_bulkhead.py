import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

import pytest
from circuit_breaker_functions.bulkhead import Bulkhead


def test_bulkhead_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with single call.
    """
    bulkhead = Bulkhead(max_concurrent=3)

    def work() -> str:
        return "completed"

    result = bulkhead.execute(work)
    assert result == "completed"
    assert bulkhead.current_concurrent == 0


def test_bulkhead_case_2_multiple_sequential_calls() -> None:
    """
    Test case 2: Multiple sequential calls within limit.
    """
    bulkhead = Bulkhead(max_concurrent=2)

    def work(value: int) -> int:
        return value * 2

    results = []
    for i in range(5):
        result = bulkhead.call(work, i)
        results.append(result)

    assert results == [0, 2, 4, 6, 8]
    assert bulkhead.current_concurrent == 0


def test_bulkhead_case_3_with_args_and_kwargs() -> None:
    """
    Test case 3: Bulkhead with function arguments.
    """
    bulkhead = Bulkhead(max_concurrent=3)

    def process(a: int, b: int, multiply: bool = True) -> int:
        if multiply:
            return a * b
        return a + b

    result1 = bulkhead.execute(process, 3, 4)
    assert result1 == 12

    result2 = bulkhead.execute(process, 3, 4, multiply=False)
    assert result2 == 7


def test_bulkhead_case_4_concurrent_execution_within_limit() -> None:
    """
    Test case 4: Concurrent executions within max_concurrent limit.
    """
    bulkhead = Bulkhead(max_concurrent=3)
    results = []

    def slow_work(value: int) -> int:
        time.sleep(0.1)
        return value * 2

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(bulkhead.call, slow_work, i) for i in range(3)]
        for future in futures:
            results.append(future.result(timeout=2))

    assert sorted(results) == [0, 2, 4]
    assert bulkhead.current_concurrent == 0


def test_bulkhead_case_5_edge_case_max_concurrent_reached() -> None:
    """
    Test case 5: Timeout when max_concurrent is reached.
    """
    bulkhead = Bulkhead(max_concurrent=2, timeout=0.2)

    def slow_work() -> str:
        time.sleep(0.5)
        return "done"

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit 3 tasks when only 2 can run concurrently
        futures = [executor.submit(bulkhead.call, slow_work) for _ in range(3)]

        # First two should succeed or timeout, third should timeout waiting for semaphore
        results = []
        errors = []
        for future in futures:
            try:
                results.append(future.result(timeout=1))
            except Exception as e:
                errors.append(e)

        # At least one should have timed out
        assert len(errors) > 0 or len(results) < 3


def test_bulkhead_case_6_edge_case_zero_timeout() -> None:
    """
    Test case 6: Immediate timeout with zero timeout value.
    """
    bulkhead = Bulkhead(max_concurrent=1, timeout=0.0)

    def work() -> str:
        time.sleep(0.01)
        return "done"

    # First call acquires semaphore
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(bulkhead.execute, work)
        time.sleep(0.005)  # Ensure first call is running

        # Second call should timeout immediately
        future2 = executor.submit(bulkhead.execute, work)

        try:
            future1.result(timeout=1)
        except:
            pass

        with pytest.raises((TimeoutError, FuturesTimeoutError)):
            future2.result(timeout=0.5)


def test_bulkhead_case_7_edge_case_function_raises_exception() -> None:
    """
    Test case 7: Semaphore released when function raises exception.
    """
    bulkhead = Bulkhead(max_concurrent=2)

    def failing_work() -> None:
        raise ValueError("Task failed")

    with pytest.raises(ValueError, match="Task failed"):
        bulkhead.call(failing_work)

    # Semaphore should be released, next call should work
    def success_work() -> str:
        return "success"

    result = bulkhead.call(success_work)
    assert result == "success"


def test_bulkhead_case_8_edge_case_single_concurrent() -> None:
    """
    Test case 8: Bulkhead with max_concurrent=1.
    """
    bulkhead = Bulkhead(max_concurrent=1)

    def work(value: int) -> int:
        time.sleep(0.05)
        return value

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(bulkhead.call, work, i) for i in range(2)]
        results = [f.result(timeout=2) for f in futures]

    assert sorted(results) == [0, 1]


def test_bulkhead_case_9_edge_case_stats_tracking() -> None:
    """
    Test case 9: Statistics tracking with get_stats.
    """
    bulkhead = Bulkhead(max_concurrent=3)

    def work() -> str:
        return "done"

    # Execute some tasks
    bulkhead.call(work)
    bulkhead.call(work)

    # Check active_count property
    assert bulkhead.active_count == 0
    assert bulkhead.max_concurrent == 3
    assert bulkhead.available_slots == 3


def test_bulkhead_case_10_edge_case_properties() -> None:
    \"\"\"
    Test case 10: Test active_count and available_slots properties.
    \"\"\"
    bulkhead = Bulkhead(max_concurrent=3)

    def work() -> str:
        return \"done\"

    # Initially, no active operations
    assert bulkhead.active_count == 0
    assert bulkhead.available_slots == 3

    # After call completes, count should be back to 0
    result = bulkhead.call(work)
    assert result == \"done\"
    assert bulkhead.active_count == 0
    assert bulkhead.available_slots == 3


def test_bulkhead_case_11_type_error_invalid_max_concurrent() -> None:
    """
    Test case 11: TypeError for invalid max_concurrent type.
    """
    with pytest.raises(TypeError, match="max_concurrent must be an integer"):
        Bulkhead(max_concurrent="3")  # type: ignore[arg-type]


def test_bulkhead_case_12_value_error_zero_max_concurrent() -> None:
    """
    Test case 12: ValueError for zero max_concurrent.
    """
    with pytest.raises(ValueError, match="max_concurrent must be positive"):
        Bulkhead(max_concurrent=0)


def test_bulkhead_case_13_value_error_negative_max_concurrent() -> None:
    """
    Test case 13: ValueError for negative max_concurrent.
    """
    with pytest.raises(ValueError, match="max_concurrent must be positive"):
        Bulkhead(max_concurrent=-1)


def test_bulkhead_case_14_type_error_invalid_timeout() -> None:
    """
    Test case 14: TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number or None"):
        Bulkhead(max_concurrent=3, timeout="5")  # type: ignore[arg-type]


def test_bulkhead_case_15_value_error_negative_timeout() -> None:
    """
    Test case 15: ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        Bulkhead(max_concurrent=3, timeout=-1.0)


def test_bulkhead_case_16_type_error_non_callable() -> None:
    """
    Test case 16: TypeError for non-callable function.
    """
    bulkhead = Bulkhead(max_concurrent=3)

    with pytest.raises(TypeError, match="func must be callable"):
        bulkhead.call("not_a_function")  # type: ignore[arg-type]
