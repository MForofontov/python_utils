import os

def create_directory(dir: str) -> bool:
    """
    Creates a directory based on the input dir path.

    Parameters
    ----------
    dir : str
        Directory path.

    Returns
    -------
    bool
        True if the directory was created, False if it already exists.
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
        return True
    else:
        return False