import os


def get_paths_in_directory(directory: str, type_: str) -> list[str]:
    """
    Get all paths of items in the specified directory filtered by type.

    This function lists all items (files, directories, or both) in the given directory
    and returns their full paths. The items to be listed can be filtered by specifying
    a type: 'files' for files only, 'directories' for directories only, or 'all' for both.

    Parameters
    ----------
    directory : str
        The path to the directory from which to retrieve item paths.
    type_ : str
        The type of items to include in the output list. Valid options are:
        - 'files': Include only files.
        - 'directories': Include only directories.
        - 'all': Include both files and directories.

    Returns
    -------
    List[str]
        A list containing the full paths of the items in the directory, filtered by the specified type.

    Raises
    ------
    ValueError
        If the `type_` parameter is not one of the valid options ('files', 'directories', 'all').
    """
    if type_ == "files":
        if_type = os.path.isfile
    elif type_ == "directories":
        if_type = os.path.isdir
    elif type_ == "all":
        if_type = os.path.exists
    else:
        raise ValueError(f"Invalid type: {type_}")

    all_items: list[str] = os.listdir(directory)
    file_paths: list[str] = [
        os.path.join(directory, item)
        for item in all_items
        if if_type(os.path.join(directory, item))
    ]

    return file_paths

__all__ = ['get_paths_in_directory']
