import os


def check_and_delete_file(file: str) -> None:
    """
    Deletes a file based on the input file path.

    Parameters
    ----------
    file : str
        File path.

    Returns
    -------
    None
    """
    if os.path.isfile(file):
        os.remove(file)
