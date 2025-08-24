import shutil


def get_tool_path(name: str) -> str | None:
    """
    Get the path of the specified tool.

    Parameters
    ----------
    name : str
        The name of the tool.

    Returns
    -------
    Optional[str]
        The path of the tool if it is found in the PATH. If the tool is not found, returns None.
    """
    return shutil.which(name)


__all__ = ['get_tool_path']
