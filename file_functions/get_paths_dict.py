import os


def get_paths_dict(directory: str, type_: str) -> dict[str, str]:
    """
    Get a dictionary where keys are filenames and values are file paths within the directory,
    filtered by the specified type: files, directories, or all items.

    Parameters
    ----------
    directory : str
        The path to the directory from which to retrieve file paths.
    type_ : str
        The type of items to include in the output dictionary. Valid options are:
        - 'files': Include only files.
        - 'directories': Include only directories.
        - 'all': Include both files and directories.

    Returns
    -------
    Dict[str, str]
        A dictionary with filenames as keys and their full paths as values. The contents
        are filtered based on the `type_` parameter.

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

    paths_dict: dict[str, str] = {}
    all_items: list[str] = os.listdir(directory)

    for filename in all_items:
        file_path: str = os.path.join(directory, filename)
        if if_type(file_path):
            paths_dict[filename] = file_path

    return paths_dict
