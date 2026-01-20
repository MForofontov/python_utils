"""Directory listing utilities."""

import os


def list_directories(directory_path: str, include_hidden: bool = False) -> list[str]:
    """
    List all directories in a given path.

    Parameters
    ----------
    directory_path : str
        Path to the parent directory.
    include_hidden : bool, optional
        Include hidden directories (starting with .) (by default False).

    Returns
    -------
    list[str]
        List of directory names.

    Raises
    ------
    TypeError
        If directory_path is not a string.
    FileNotFoundError
        If directory does not exist.
    NotADirectoryError
        If path is not a directory.

    Examples
    --------
    >>> dirs = list_directories('/tmp')
    >>> isinstance(dirs, list)
    True
    """
    if not isinstance(directory_path, str):
        raise TypeError("directory_path must be a string")

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory does not exist: {directory_path}")

    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Path is not a directory: {directory_path}")

    directories = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            if include_hidden or not item.startswith("."):
                directories.append(item)

    return sorted(directories)


__all__ = ["list_directories"]
