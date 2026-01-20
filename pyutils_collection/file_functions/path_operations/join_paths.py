"""Path joining utilities."""

import os


def join_paths(parent_path: str, child_paths: list[str]) -> str:
    """
    Create a path by joining a parent directory and a list of child paths.

    Parameters
    ----------
    parent_path : str
        The parent directory path.
    child_paths : list[str]
        A list of child path segments to join with the parent path.

    Returns
    -------
    str
        The joined path.

    Raises
    ------
    None

    Examples
    --------
    >>> join_paths('/home/user', ['docs', 'file.txt'])
    '/home/user/docs/file.txt'
    """
    joined_paths: str = os.path.join(parent_path, *child_paths)
    return joined_paths


__all__ = ["join_paths"]
