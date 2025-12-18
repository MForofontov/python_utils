"""
Composable data transformation pipeline builder.
"""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")
R = TypeVar("R")


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
