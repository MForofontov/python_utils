import os
import shutil


def cleanup(directory: str, exclude: list[str]) -> None:
    """
    Clean up a directory by removing all files and subdirectories except those
    specified in the exclusion list.

    Parameters
    ----------
    directory : str
        The path to the directory to clean up.
    exclude : list[str]
        A list of filenames or subdirectory names to exclude from removal.
        Entries may be provided either as absolute paths or names relative to
        ``directory``. Absolute paths are normalized to their base names before
        comparison. For example, both ``"important.txt"`` and
        ``"/tmp/project/important.txt"`` will preserve the same file when
        ``directory`` is ``/tmp/project``.

    Returns
    -------
    None
    """
    normalized_exclude = {os.path.basename(os.path.normpath(path)) for path in exclude}

    for item in os.listdir(directory):
        if item not in normalized_exclude:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


__all__ = ["cleanup"]
