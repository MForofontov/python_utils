"""
Composable data transformation pipeline builder.
"""

import logging
from collections.abc import Callable, Iterable
from functools import reduce
from itertools import groupby
from typing import Any, TypeVar

T = TypeVar("T")
R = TypeVar("R")
K = TypeVar("K")


class Pipeline:
    """
    Composable data transformation pipeline.

    Enables building functional data processing pipelines where each step
    transforms the data and passes it to the next step. Supports method
    chaining for readable pipeline construction.

    Attributes
    ----------
    steps : list[Callable]
        List of transformation functions in the pipeline.

    Examples
    --------
    >>> pipeline = Pipeline()
    >>> pipeline.add_step(lambda x: x * 2)
    >>> pipeline.add_step(lambda x: x + 10)
    >>> pipeline.execute(5)
    20

    >>> # Method chaining
    >>> result = (Pipeline()
    ...     .add_step(str.upper)
    ...     .add_step(lambda s: s + '!')
    ...     .execute('hello'))
    >>> result
    'HELLO!'

    Notes
    -----
    The pipeline pattern enables:
    - Separation of concerns (each step does one thing)
    - Reusability (steps can be shared across pipelines)
    - Testability (each step can be tested independently)
    - Composability (pipelines can be combined)

    Common use cases:
    - Data ETL (Extract, Transform, Load)
    - Request/response processing
    - Text processing workflows
    - Image processing pipelines

    Complexity
    ----------
    Time: O(n) where n is number of steps, Space: O(n)
    """

    def __init__(self) -> None:
        """Initialize empty pipeline."""
        self.steps: list[Callable[[Any], Any]] = []

    def add_step(self, func: Callable[[Any], Any]) -> "Pipeline":
        """
        Add a transformation step to the pipeline.

        Parameters
        ----------
        func : Callable[[Any], Any]
            Transformation function to add.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If func is not callable.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_step(lambda x: x + 1)
        <...Pipeline object...>
        >>> p.execute(5)
        6
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        self.steps.append(func)
        return self

    def execute(self, data: T) -> Any:
        """
        Execute pipeline on input data.

        Parameters
        ----------
        data : T
            Input data to process.

        Returns
        -------
        Any
            Transformed data after all steps.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_step(lambda x: x * 2)
        <...Pipeline object...>
        >>> p.add_step(lambda x: x + 1)
        <...Pipeline object...>
        >>> p.execute(10)
        21
        """
        result = data
        for step in self.steps:
            result = step(result)
        return result

    def add_conditional_step(
        self,
        condition: Callable[[Any], bool],
        true_func: Callable[[Any], Any],
        false_func: Callable[[Any], Any] | None = None,
    ) -> "Pipeline":
        """
        Add a conditional step that branches based on condition.

        Parameters
        ----------
        condition : Callable[[Any], bool]
            Function that returns True/False.
        true_func : Callable[[Any], Any]
            Function to apply if condition is True.
        false_func : Callable[[Any], Any] | None, optional
            Function to apply if condition is False (by default None, passes through).

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If parameters are not callable.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_conditional_step(
        ...     lambda x: x > 0,
        ...     lambda x: x * 2,
        ...     lambda x: x * -1
        ... )
        <...Pipeline object...>
        >>> p.execute(5)
        10
        >>> p.execute(-5)
        5
        """
        if not callable(condition):
            raise TypeError(
                f"condition must be callable, got {type(condition).__name__}"
            )
        if not callable(true_func):
            raise TypeError(
                f"true_func must be callable, got {type(true_func).__name__}"
            )
        if false_func is not None and not callable(false_func):
            raise TypeError(
                f"false_func must be callable or None, got {type(false_func).__name__}"
            )

        def conditional_step(data: Any) -> Any:
            if condition(data):
                return true_func(data)
            elif false_func is not None:
                return false_func(data)
            else:
                return data

        self.steps.append(conditional_step)
        return self

    def map_step(self, func: Callable[[Any], Any]) -> "Pipeline":
        """
        Add a step that maps function over iterable data.

        Parameters
        ----------
        func : Callable[[Any], Any]
            Function to map over each element.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If func is not callable.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.map_step(lambda x: x * 2)
        <...Pipeline object...>
        >>> list(p.execute([1, 2, 3]))
        [2, 4, 6]
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        def map_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError(f"Data must be iterable for map_step")
            return map(func, data)

        self.steps.append(map_func)
        return self

    def filter_step(self, predicate: Callable[[Any], bool]) -> "Pipeline":
        """
        Add a step that filters iterable data.

        Parameters
        ----------
        predicate : Callable[[Any], bool]
            Function that returns True to keep element.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If predicate is not callable.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.filter_step(lambda x: x > 2)
        <...Pipeline object...>
        >>> list(p.execute([1, 2, 3, 4]))
        [3, 4]
        """
        if not callable(predicate):
            raise TypeError(
                f"predicate must be callable, got {type(predicate).__name__}"
            )

        def filter_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError(f"Data must be iterable for filter_step")
            return filter(predicate, data)

        self.steps.append(filter_func)
        return self

    def reduce_step(
        self,
        func: Callable[[Any, Any], Any],
        initial: Any = None,
    ) -> "Pipeline":
        """
        Add a step that reduces iterable to single value.

        Parameters
        ----------
        func : Callable[[Any, Any], Any]
            Binary function to reduce with (accumulator, element).
        initial : Any, optional
            Initial value for reduction (by default None).

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If func is not callable.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.reduce_step(lambda acc, x: acc + x, 0)
        <...Pipeline object...>
        >>> p.execute([1, 2, 3, 4])
        10
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        def reduce_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError("Data must be iterable for reduce_step")
            if initial is not None:
                return reduce(func, data, initial)
            else:
                return reduce(func, data)

        self.steps.append(reduce_func)
        return self

    def add_tap_step(
        self,
        func: Callable[[Any], None],
        logger: logging.Logger | None = None,
    ) -> "Pipeline":
        """
        Add a step that observes data without modifying it.

        Useful for logging, debugging, or side effects while data flows through.

        Parameters
        ----------
        func : Callable[[Any], None]
            Function to call with data (return value ignored).
        logger : logging.Logger | None, optional
            Logger to use if func raises exception (by default None).

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If func is not callable.

        Examples
        --------
        >>> collected = []
        >>> p = Pipeline()
        >>> p.add_step(lambda x: x * 2)
        <...Pipeline object...>
        >>> p.add_tap_step(collected.append)
        <...Pipeline object...>
        >>> p.add_step(lambda x: x + 1)
        <...Pipeline object...>
        >>> result = p.execute(5)
        >>> collected
        [10]
        >>> result
        11
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")
        if logger is not None and not isinstance(logger, logging.Logger):
            raise TypeError("logger must be an instance of logging.Logger or None")

        def tap_func(data: Any) -> Any:
            try:
                func(data)
            except Exception as e:
                if logger:
                    logger.error(f"Error in tap_step: {e}", exc_info=True)
                # Continue pipeline even if tap fails
            return data

        self.steps.append(tap_func)
        return self

    def add_flatten_step(self, levels: int = 1) -> "Pipeline":
        """
        Add a step that flattens nested iterables.

        Parameters
        ----------
        levels : int, optional
            Number of nesting levels to flatten (by default 1).
            Use -1 to flatten all levels.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If levels is not an integer.
        ValueError
            If levels is less than -1 or is 0.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_flatten_step()
        <...Pipeline object...>
        >>> list(p.execute([[1, 2], [3, 4]]))
        [1, 2, 3, 4]

        >>> # Multiple levels
        >>> p2 = Pipeline()
        >>> p2.add_flatten_step(levels=2)
        <...Pipeline object...>
        >>> list(p2.execute([[[1, 2]], [[3, 4]]]))
        [1, 2, 3, 4]
        """
        if not isinstance(levels, int):
            raise TypeError(f"levels must be an integer, got {type(levels).__name__}")
        if levels < -1 or levels == 0:
            raise ValueError("levels must be -1 (infinite) or positive integer")

        def flatten_func(data: Any) -> Any:
            if not hasattr(data, "__iter__") or isinstance(data, (str, bytes)):
                raise TypeError("Data must be iterable for flatten_step")

            def flatten(items: Any, depth: int) -> Iterable[Any]:
                for item in items:
                    if (
                        depth != 0
                        and hasattr(item, "__iter__")
                        and not isinstance(item, (str, bytes))
                    ):
                        yield from flatten(item, depth - 1 if depth > 0 else -1)
                    else:
                        yield item

            return flatten(data, levels)

        self.steps.append(flatten_func)
        return self

    def add_batch_step(self, batch_size: int) -> "Pipeline":
        """
        Add a step that batches items into fixed-size groups.

        Parameters
        ----------
        batch_size : int
            Number of items per batch.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If batch_size is not an integer.
        ValueError
            If batch_size is less than 1.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_batch_step(2)
        <...Pipeline object...>
        >>> list(p.execute([1, 2, 3, 4, 5]))
        [[1, 2], [3, 4], [5]]
        """
        if not isinstance(batch_size, int):
            raise TypeError(
                f"batch_size must be an integer, got {type(batch_size).__name__}"
            )
        if batch_size < 1:
            raise ValueError(f"batch_size must be at least 1, got {batch_size}")

        def batch_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError("Data must be iterable for batch_step")

            batch = []
            for item in data:
                batch.append(item)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:  # Yield remaining items
                yield batch

        self.steps.append(batch_func)
        return self

    def add_distinct_step(self, key: Callable[[Any], Any] | None = None) -> "Pipeline":
        """
        Add a step that removes duplicate items.

        Parameters
        ----------
        key : Callable[[Any], Any] | None, optional
            Function to compute comparison key (by default None uses item itself).

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If key is not callable or None.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_distinct_step()
        <...Pipeline object...>
        >>> list(p.execute([1, 2, 2, 3, 1, 4]))
        [1, 2, 3, 4]

        >>> # With key function
        >>> p2 = Pipeline()
        >>> p2.add_distinct_step(key=lambda x: x.lower())
        <...Pipeline object...>
        >>> list(p2.execute(['A', 'a', 'B', 'b', 'C']))
        ['A', 'B', 'C']
        """
        if key is not None and not callable(key):
            raise TypeError(f"key must be callable or None, got {type(key).__name__}")

        def distinct_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError("Data must be iterable for distinct_step")

            seen = set()
            for item in data:
                k = key(item) if key else item
                # Handle unhashable types
                try:
                    if k not in seen:
                        seen.add(k)
                        yield item
                except TypeError:
                    # For unhashable types, use list comparison (slower)
                    if k not in [key(x) if key else x for x in seen]:
                        seen.add(k if key else item)
                        yield item

        self.steps.append(distinct_func)
        return self

    def group_by_step(
        self,
        key: Callable[[Any], K],
        sort_first: bool = True,
    ) -> "Pipeline":
        """
        Add a step that groups consecutive items by key.

        Parameters
        ----------
        key : Callable[[Any], K]
            Function to compute grouping key.
        sort_first : bool, optional
            Whether to sort data before grouping (by default True).
            Note: groupby only groups consecutive items with same key.

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If key is not callable or sort_first is not boolean.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.group_by_step(lambda x: x % 2)
        <...Pipeline object...>
        >>> result = list(p.execute([1, 2, 3, 4, 5, 6]))
        >>> [(k, list(g)) for k, g in result]
        [(0, [2, 4, 6]), (1, [1, 3, 5])]
        """
        if not callable(key):
            raise TypeError(f"key must be callable, got {type(key).__name__}")
        if not isinstance(sort_first, bool):
            raise TypeError(
                f"sort_first must be a boolean, got {type(sort_first).__name__}"
            )

        def group_func(data: Any) -> Any:
            if not hasattr(data, "__iter__"):
                raise TypeError("Data must be iterable for group_by_step")

            items = list(data)
            if sort_first:
                items = sorted(items, key=key)

            return groupby(items, key=key)

        self.steps.append(group_func)
        return self

    def add_error_handler(
        self,
        handler: Callable[[Exception, Any], Any],
        exception_types: tuple[type[Exception], ...] = (Exception,),
    ) -> "Pipeline":
        """
        Add error handling to the pipeline.

        Catches exceptions from subsequent steps and handles them.

        Parameters
        ----------
        handler : Callable[[Exception, Any], Any]
            Function that takes (exception, data) and returns recovery value.
        exception_types : tuple[type[Exception], ...], optional
            Tuple of exception types to catch (by default catches all Exception).

        Returns
        -------
        Pipeline
            Self for method chaining.

        Raises
        ------
        TypeError
            If parameters are not of correct type.

        Examples
        --------
        >>> p = Pipeline()
        >>> p.add_step(lambda x: 10 / x)
        <...Pipeline object...>
        >>> p.add_error_handler(lambda e, data: 0)  # Return 0 on error
        <...Pipeline object...>
        >>> p.execute(0)
        0
        """
        if not callable(handler):
            raise TypeError(f"handler must be callable, got {type(handler).__name__}")
        if not isinstance(exception_types, tuple):
            raise TypeError(
                f"exception_types must be a tuple, got {type(exception_types).__name__}"
            )
        for exc_type in exception_types:
            if not isinstance(exc_type, type) or not issubclass(exc_type, Exception):
                raise TypeError(
                    f"exception_types must contain Exception types, got {exc_type}"
                )

        # Wrap all remaining steps in error handler
        remaining_steps = self.steps.copy()
        self.steps = self.steps[:-len(remaining_steps)] if remaining_steps else []

        def error_handler_func(data: Any) -> Any:
            try:
                result = data
                for step in remaining_steps:
                    result = step(result)
                return result
            except exception_types as e:
                return handler(e, data)

        self.steps.append(error_handler_func)
        return self

    def combine(self, other: "Pipeline") -> "Pipeline":
        """
        Combine this pipeline with another pipeline.

        Parameters
        ----------
        other : Pipeline
            Another pipeline to append.

        Returns
        -------
        Pipeline
            New pipeline combining both.

        Raises
        ------
        TypeError
            If other is not a Pipeline.

        Examples
        --------
        >>> p1 = Pipeline().add_step(lambda x: x * 2)
        >>> p2 = Pipeline().add_step(lambda x: x + 1)
        >>> p3 = p1.combine(p2)
        >>> p3.execute(5)
        11
        """
        if not isinstance(other, Pipeline):
            raise TypeError(f"other must be a Pipeline, got {type(other).__name__}")

        combined = Pipeline()
        combined.steps = self.steps + other.steps
        return combined

    def __call__(self, data: T) -> Any:
        """
        Make pipeline callable.

        Allows using pipeline as a function.

        Examples
        --------
        >>> p = Pipeline().add_step(lambda x: x * 2)
        >>> p(5)
        10
        """
        return self.execute(data)


def pipeline_builder(*steps: Callable[[Any], Any]) -> Pipeline:
    """
    Build a pipeline from a sequence of transformation functions.

    Convenience function to create a pipeline with multiple steps
    at once.

    Parameters
    ----------
    *steps : Callable[[Any], Any]
        Variable number of transformation functions.

    Returns
    -------
    Pipeline
        Pipeline with all steps added.

    Raises
    ------
    TypeError
        If any step is not callable.

    Examples
    --------
    >>> p = pipeline_builder(
    ...     lambda x: x * 2,
    ...     lambda x: x + 10,
    ...     lambda x: x / 2
    ... )
    >>> p.execute(5)
    10.0

    >>> # Can still add more steps
    >>> p.add_step(lambda x: int(x))
    <...Pipeline object...>
    >>> p.execute(5)
    10

    Notes
    -----
    This is a convenience function for creating pipelines. It's
    equivalent to:
    
    >>> p = Pipeline()
    >>> for step in steps:
    ...     p.add_step(step)

    Complexity
    ----------
    Time: O(n) where n is number of steps, Space: O(n)
    """
    pipeline = Pipeline()
    for step in steps:
        if not callable(step):
            raise TypeError(f"All steps must be callable, got {type(step).__name__}")
        pipeline.add_step(step)
    return pipeline


__all__ = ["Pipeline", "pipeline_builder"]
