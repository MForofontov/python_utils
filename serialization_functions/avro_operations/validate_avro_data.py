"""
Validate data against Avro schema.
"""

from typing import Any


def validate_avro_data(
    data: list[dict[str, Any]],
    schema: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate data against Avro schema.

    Parameters
    ----------
    data : list[dict[str, Any]]
        List of dictionaries to validate.
    schema : dict[str, Any]
        Avro schema definition.

    Returns
    -------
    tuple[bool, str]
        (is_valid, error_message). error_message is empty if valid.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ImportError
        If fastavro is not installed.

    Examples
    --------
    >>> schema = {'type': 'record', 'name': 'Person', 'fields': [
    ...     {'name': 'name', 'type': 'string'},
    ...     {'name': 'age', 'type': 'int'}
    ... ]}
    >>> data = [{'name': 'Alice', 'age': 30}]
    >>> is_valid, error = validate_avro_data(data, schema)
    >>> is_valid
    True

    >>> bad_data = [{'name': 'Bob', 'age': 'thirty'}]
    >>> is_valid, error = validate_avro_data(bad_data, schema)
    >>> is_valid
    False

    Notes
    -----
    Requires fastavro package.
    Checks type compatibility and required fields.

    Complexity
    ----------
    Time: O(n*m), Space: O(1), where n is rows, m is columns
    """
    try:
        from fastavro import validate_many
    except ImportError as e:
        raise ImportError("fastavro is required. Install with: pip install fastavro") from e
    
    if not isinstance(data, list):
        raise TypeError(f"data must be a list, got {type(data).__name__}")
    
    if not all(isinstance(item, dict) for item in data):
        raise TypeError("all elements in data must be dictionaries")
    
    if not isinstance(schema, dict):
        raise TypeError(f"schema must be a dict, got {type(schema).__name__}")
    
    try:
        # validate_many returns True if all valid, raises exception otherwise
        validate_many(data, schema)
        return (True, "")
    except Exception as e:
        return (False, str(e))


__all__ = ['validate_avro_data']
