import multiprocessing_functions.parallel_progress_bar as ppb


def incr(x: int) -> int:
    return x + 1


def test_parallel_progress_bar_cpu_count_minimum(monkeypatch) -> None:
    monkeypatch.setattr(ppb, "cpu_count", lambda: 1)
    assert ppb.parallel_progress_bar(incr, [1, 2, 3]) == [2, 3, 4]

