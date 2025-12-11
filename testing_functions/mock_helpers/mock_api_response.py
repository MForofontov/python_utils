"""
Create mock HTTP API response.
"""

from typing import Any
from unittest.mock import Mock


def mock_api_response(
    status_code: int = 200,
    data: Any = None,
    headers: dict[str, str] | None = None,
) -> Mock:
    """
    Create a mock HTTP API response.

    Parameters
    ----------
    status_code : int, optional
        HTTP status code (by default 200).
    data : Any, optional
        Response data (by default None).
    headers : dict[str, str] | None, optional
        Response headers (by default None).

    Returns
    -------
    Mock
        Mock response object.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If status_code is invalid.

    Examples
    --------
    >>> response = mock_api_response(200, {"key": "value"})
    >>> response.status_code
    200
    >>> response.json()
    {'key': 'value'}

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(status_code, int):
        raise TypeError(f"status_code must be an integer, got {type(status_code).__name__}")
    if headers is not None and not isinstance(headers, dict):
        raise TypeError(f"headers must be a dict or None, got {type(headers).__name__}")
    
    if not (100 <= status_code < 600):
        raise ValueError(f"status_code must be between 100 and 599, got {status_code}")
    
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.headers = headers or {}
    mock_response.json.return_value = data
    mock_response.text = str(data) if data is not None else ""
    
    return mock_response


__all__ = ['mock_api_response']
