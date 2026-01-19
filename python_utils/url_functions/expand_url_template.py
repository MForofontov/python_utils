"""
URL template expansion (RFC 6570).
"""

import re
from typing import Any


def expand_url_template(
    template: str,
    variables: dict[str, Any],
    strict: bool = False,
) -> str:
    """
    Expand URL template with variables (RFC 6570 subset).

    Implements URI template expansion for building URLs from templates.
    Supports basic variable substitution with various operators.
    Adds workflow logic for common templating patterns.

    Parameters
    ----------
    template : str
        URL template with variable placeholders like "{var}".
    variables : dict[str, Any]
        Variable values to substitute.
    strict : bool, optional
        Raise error for undefined variables (by default False).

    Returns
    -------
    str
        Expanded URL.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If template is empty or invalid.

    Examples
    --------
    >>> expand_url_template("/users/{user_id}", {"user_id": 123})
    '/users/123'
    >>> expand_url_template("/search{?q,page}", {"q": "python", "page": 2})
    '/search?q=python&page=2'
    >>> expand_url_template("/repos{/owner,repo}", {"owner": "python", "repo": "cpython"})
    '/repos/python/cpython'
    >>> expand_url_template("/api/{version}/users", {"version": "v2"})
    '/api/v2/users'

    Notes
    -----
    Implements subset of RFC 6570:
    - Simple expansion: {var}
    - Query expansion: {?var,var2}
    - Path expansion: {/var,var2}
    - Fragment expansion: {#var}

    Adds workflow logic for:
    - Type coercion of variable values
    - List variable handling
    - Undefined variable handling (strict mode)
    - URL encoding of values

    Common use cases:
    - REST API URL building
    - Hypermedia links (HATEOAS)
    - Dynamic route generation
    - API client URL construction

    Complexity
    ----------
    Time: O(n + m*k) where n is template length, m is variables, k is avg length,
    Space: O(n + m*k)
    """
    # Input validation
    if not isinstance(template, str):
        raise TypeError(f"template must be a string, got {type(template).__name__}")
    if not isinstance(variables, dict):
        raise TypeError(f"variables must be a dict, got {type(variables).__name__}")
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be a bool, got {type(strict).__name__}")

    if not template:
        raise ValueError("template cannot be empty")

    # Pattern to match template variables
    pattern = re.compile(r"\{([#/\?]?)([^}]+)\}")

    def replace_variable(match: re.Match[str]) -> str:
        """Replace a single template variable."""
        operator = match.group(1)
        var_spec = match.group(2)

        # Split multiple variables
        var_names = [v.strip() for v in var_spec.split(",")]

        # Process variables based on operator
        if operator == "?":
            # Query string expansion
            parts = []
            for var_name in var_names:
                if var_name in variables:
                    value = variables[var_name]
                    if isinstance(value, list):
                        for item in value:
                            parts.append(f"{var_name}={_encode_value(item)}")
                    else:
                        parts.append(f"{var_name}={_encode_value(value)}")
                elif strict:
                    raise ValueError(f"Undefined variable: {var_name}")

            return "?" + "&".join(parts) if parts else ""

        elif operator == "/":
            # Path expansion
            parts = []
            for var_name in var_names:
                if var_name in variables:
                    value = variables[var_name]
                    if isinstance(value, list):
                        parts.extend(_encode_value(item) for item in value)
                    else:
                        parts.append(_encode_value(value))
                elif strict:
                    raise ValueError(f"Undefined variable: {var_name}")

            return "/" + "/".join(parts) if parts else ""

        elif operator == "#":
            # Fragment expansion
            parts = []
            for var_name in var_names:
                if var_name in variables:
                    value = variables[var_name]
                    if isinstance(value, list):
                        parts.extend(str(item) for item in value)
                    else:
                        parts.append(str(value))
                elif strict:
                    raise ValueError(f"Undefined variable: {var_name}")

            return "#" + ",".join(parts) if parts else ""

        else:
            # Simple expansion
            parts = []
            for var_name in var_names:
                if var_name in variables:
                    value = variables[var_name]
                    if isinstance(value, list):
                        parts.extend(_encode_value(item) for item in value)
                    else:
                        parts.append(_encode_value(value))
                elif strict:
                    raise ValueError(f"Undefined variable: {var_name}")

            return ",".join(parts) if parts else ""

    # Expand all variables in template
    result = pattern.sub(replace_variable, template)
    return result


def _encode_value(value: Any) -> str:
    """Encode a value for URL inclusion."""
    from urllib.parse import quote

    str_value = str(value)
    # Use quote with safe='' to encode all special characters
    return quote(str_value, safe="")


__all__ = ["expand_url_template"]
