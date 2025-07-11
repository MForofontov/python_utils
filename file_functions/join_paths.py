import os

def join_paths(parent_path: str, child_paths: list[str]) -> str:
    """
    Create a path by joining a parent directory and a list of child paths.

    Parameters
    ----------
    parent_path : str
        The parent directory path.
    child_paths : List[str]
        A list of child paths to join with the parent path.

    Returns
    -------
    str
        The joined path.
    """
    joined_paths: str = os.path.join(parent_path, *child_paths)
    return joined_paths