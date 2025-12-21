"""Command existence check in system PATH."""

import shutil


def check_command_exists(command: str) -> bool:
    """
    Check if a command exists in the system PATH.

    Parameters
    ----------
    command : str
        Name of the command to check.

    Returns
    -------
    bool
        True if command exists in PATH, False otherwise.

    Raises
    ------
    TypeError
        If command is not a string.
    ValueError
        If command is empty.

    Examples
    --------
    >>> check_command_exists('python')
    True
    >>> check_command_exists('nonexistent_command_12345')
    False

    Notes
    -----
    This function uses shutil.which() which searches for executables
    in the directories listed in the PATH environment variable.

    Complexity
    ----------
    Time: O(n) where n is number of directories in PATH
    Space: O(1)
    """
    if not isinstance(command, str):
        raise TypeError(f"command must be a string, got {type(command).__name__}")
    
    if not command:
        raise ValueError("command cannot be empty")
    
    return shutil.which(command) is not None


__all__ = ['check_command_exists']
