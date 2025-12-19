import pytest
from cli_functions.check_command_exists import check_command_exists


def test_check_command_exists_python_exists() -> None:
    """
    Test case 1: Test check_command_exists with python command.
    """
    result = check_command_exists('python')
    assert isinstance(result, bool)
    # Python should exist (either python or python3)
    assert result is True or check_command_exists('python3') is True


def test_check_command_exists_nonexistent_command() -> None:
    """
    Test case 2: Test check_command_exists with nonexistent command.
    """
    result = check_command_exists('nonexistent_command_xyz_12345')
    assert result is False


def test_check_command_exists_common_commands() -> None:
    """
    Test case 3: Test check_command_exists with common commands.
    """
    # At least one of these should exist on most systems
    common_commands = ['ls', 'dir', 'echo', 'sh', 'bash', 'cmd']
    results = [check_command_exists(cmd) for cmd in common_commands]
    assert any(results), "At least one common command should exist"


def test_check_command_exists_invalid_type_error() -> None:
    """
    Test case 4: Invalid command type raises TypeError.
    """
    with pytest.raises(TypeError, match="command must be a string"):
        check_command_exists(123)
    
    with pytest.raises(TypeError):
        check_command_exists(None)


def test_check_command_exists_empty_string_error() -> None:
    """
    Test case 5: Empty command string raises ValueError.
    """
    with pytest.raises(ValueError, match="command cannot be empty"):
        check_command_exists('')


def test_check_command_exists_consistency() -> None:
    """
    Test case 6: Multiple calls return consistent results.
    """
    result1 = check_command_exists('python')
    result2 = check_command_exists('python')
    assert result1 == result2
