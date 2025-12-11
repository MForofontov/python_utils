"""
Create mock object with specified attributes.
"""

from typing import Any
from unittest.mock import Mock


def create_mock_object(
    **attributes: Any,
) -> Mock:
    """
    Create a mock object with specified attributes.

    Parameters
    ----------
    **attributes : Any
        Attributes to set on the mock object.

    Returns
    -------
    Mock
        Mock object with specified attributes.

    Examples
    --------
    >>> mock = create_mock_object(name="test", value=42)
    >>> mock.name
    'test'
    >>> mock.value
    42

    Complexity
    ----------
    Time: O(n), Space: O(n), where n is number of attributes
    """
    mock = Mock()
    for key, value in attributes.items():
        setattr(mock, key, value)
    return mock


__all__ = ['create_mock_object']
