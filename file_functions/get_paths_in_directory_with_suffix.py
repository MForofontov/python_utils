import os


def get_paths_in_directory_with_suffix(directory: str, suffix: str) -> list[str]:
    """
    Get all paths of files in the specified directory that end with a given suffix.

    Parameters
    ----------
    directory : str
        Path to the directory.
    suffix : str
        The suffix that the files must end with.

    Returns
    -------
    List[str]
        List that contains all of the file paths with the specified suffix.
    """
    all_items: list[str] = os.listdir(directory)
    file_paths: list[str] = [
        os.path.join(directory, item)
        for item in all_items
        if os.path.isfile(os.path.join(directory, item)) and item.endswith(suffix)
    ]

    return file_paths
