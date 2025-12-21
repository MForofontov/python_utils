import os
import re


def expand_env_vars_in_string(s: str, default: str | None = None) -> str:
    """
    Expand environment variables in a string (e.g., "$HOME/path" or "${USER}").

    Parameters
    ----------
    s : str
        The input string containing environment variable references.
    default : str, optional
        Value to use if a variable is not found (default is empty string).

    Returns
    -------
    str
        The string with environment variables expanded.

    Examples
    --------
    >>> import os
    >>> os.environ['FOO'] = 'bar'
    >>> expand_env_vars_in_string('Value: $FOO')
    'Value: bar'
    >>> expand_env_vars_in_string('Path: $NOT_SET', default='none')
    'Path: none'
    """

    def replacer(match: re.Match[str]) -> str:
        var = match.group(1) or match.group(2)
        return os.environ.get(var, default or "")

    return re.sub(r"\$(\w+)|\${(\w+)}", replacer, s)
