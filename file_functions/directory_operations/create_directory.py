"""Directory creation utilities."""

import os


def create_directory(directory: str) -> bool:
    """
    Creates a directory based on the input directory path.

    Parameters
    ----------
    directory : str
        Directory path.

    Returns
    -------
    bool
        True if the directory was created, False if it already exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return False


__all__ = ["create_directory"]
