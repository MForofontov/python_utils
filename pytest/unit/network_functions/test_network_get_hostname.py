import pytest

pytestmark = [pytest.mark.unit, pytest.mark.network_functions]
from unittest.mock import MagicMock, patch

from python_utils.network_functions.get_hostname import get_hostname


def test_get_hostname_returns_string() -> None:
    """
    Test case 1: Function returns a string.
    """
    # Act
    result = get_hostname()

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


@patch("socket.gethostname")
def test_get_hostname_mocked_value(mock_gethostname: MagicMock) -> None:
    """
    Test case 2: Function returns mocked hostname.
    """
    # Arrange
    mock_gethostname.return_value = "test-machine"

    # Act
    result = get_hostname()

    # Assert
    assert result == "test-machine"
    mock_gethostname.assert_called_once()


@patch("socket.gethostname")
def test_get_hostname_different_names(mock_gethostname: MagicMock) -> None:
    """
    Test case 3: Test with different hostname formats.
    """
    # Arrange
    hostnames = ["localhost", "my-computer.local", "server-01", "host123"]

    for hostname in hostnames:
        mock_gethostname.return_value = hostname

        # Act
        result = get_hostname()

        # Assert
        assert result == hostname


@patch("socket.gethostname")
def test_get_hostname_with_domain(mock_gethostname: MagicMock) -> None:
    """
    Test case 4: Hostname with domain name.
    """
    # Arrange
    mock_gethostname.return_value = "mycomputer.example.com"

    # Act
    result = get_hostname()

    # Assert
    assert result == "mycomputer.example.com"
    assert "." in result


@patch("socket.gethostname")
def test_get_hostname_special_characters(mock_gethostname: MagicMock) -> None:
    """
    Test case 5: Hostname with special characters.
    """
    # Arrange
    mock_gethostname.return_value = "host-name_123"

    # Act
    result = get_hostname()

    # Assert
    assert result == "host-name_123"


def test_get_hostname_not_empty() -> None:
    """
    Test case 6: Hostname is never empty.
    """
    # Act
    result = get_hostname()

    # Assert
    assert result != ""
    assert result is not None
