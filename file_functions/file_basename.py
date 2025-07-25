import os


def file_basename(file_path: str, file_extension: bool = True) -> str:
    """
    Get the file name from a file path.

    Parameters
    ----------
    file_path : str
        The path to the file.
    file_extension : bool, optional
        Whether to include the file extension in the returned name (default is True).

    Returns
    -------
    str
        The file name extracted from the file path.
    """
    if not file_extension:
        return os.path.basename(file_path).split(".")[0]
    else:
        return os.path.basename(file_path)
