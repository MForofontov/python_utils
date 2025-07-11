from typing import Any

def try_convert_to_type(value: Any, target_type: type) -> Any:
    """
    Attempts to convert a given value to a specified type.

    Parameters
    ----------
    value : Any
        The value to be converted.
    target_type : Type
        The type to which `value` should be converted.

    Returns
    -------
    Any
        The converted value if the conversion is successful.

    Raises
    ------
    TypeError
        If target_type is not a type.
    ValueError
        If the conversion fails.
    """
    if not isinstance(target_type, type):
        raise TypeError("target_type must be a type")

    try:
        return target_type(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to convert {value} to {target_type}") from e