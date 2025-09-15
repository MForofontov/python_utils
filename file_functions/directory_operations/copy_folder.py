import os
import shutil


def copy_folder(src_folder: str, dest_folder: str) -> None:
    """
    Copy the contents of one folder to another folder.

    Parameters
    ----------
    src_folder : str
        Path to the source folder to copy.
    dest_folder : str
        Path to the destination folder where the contents will be copied.

    Returns
    -------
    None

    Notes
    -----
    - If the destination folder does not exist, it will be created.
    - The function copies the entire folder, including all subdirectories and files.
    - If the destination folder already exists, existing files will be overwritten.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)


__all__ = ["copy_folder"]
