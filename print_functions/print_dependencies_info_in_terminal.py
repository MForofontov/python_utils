import platform
import shutil

from importlib.metadata import version, PackageNotFoundError
from print_functions.print_message import print_message


def print_dependencies_info_in_terminal(dependencies):
    """
    Print the dependencies information in the terminal.

    This function prints the dependencies information in the terminal.

    Parameters
    ----------
    dependencies : list
        A list of dependencies.

    Returns
    -------
    None
    """
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width

    print_message(separator, None)
    print_message("Dependencies Information".center(terminal_width), None)
    print_message(f"Python Version: {platform.python_version()}", "info")
    for dep in dependencies:
        try:
            dep_version = version(dep)
            print_message(f"{dep} version: {dep_version}", "info")
        except PackageNotFoundError:
            print_message(f"{dep} is not installed", "warning")

    print_message(separator, None)

__all__ = ['print_dependencies_info_in_terminal']
