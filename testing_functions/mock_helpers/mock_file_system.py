"""
Create mock file system.
"""

from unittest.mock import Mock


def mock_file_system(
    files: dict[str, str],
) -> Mock:
    """
    Create a mock file system with specified files.

    Parameters
    ----------
    files : dict[str, str]
        Dictionary mapping file paths to contents.

    Returns
    -------
    Mock
        Mock file system object.

    Raises
    ------
    TypeError
        If files is not a dictionary.

    Examples
    --------
    >>> fs = mock_file_system({"/test.txt": "content"})
    >>> fs.read("/test.txt")
    'content'
    >>> fs.exists("/test.txt")
    True

    Complexity
    ----------
    Time: O(n), Space: O(n), where n is number of files
    """
    if not isinstance(files, dict):
        raise TypeError(f"files must be a dict, got {type(files).__name__}")
    
    mock_fs = Mock()
    
    def mock_read(path: str) -> str:
        if path not in files:
            raise FileNotFoundError(f"File not found: {path}")
        return files[path]
    
    def mock_exists(path: str) -> bool:
        return path in files
    
    def mock_listdir(path: str) -> list[str]:
        return [f for f in files.keys() if f.startswith(path)]
    
    mock_fs.read = mock_read
    mock_fs.exists = mock_exists
    mock_fs.listdir = mock_listdir
    mock_fs.files = files
    
    return mock_fs


__all__ = ['mock_file_system']
