"""Unit tests for file download functionality."""

import pytest
from unittest.mock import patch, Mock, mock_open
from pathlib import Path
import urllib.error
from http_functions.download_file import download_file


def test_download_file_with_empty_url():
    """Test case 1: Test download_file function with empty URL raises ValueError."""
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        download_file("", "test.txt")


def test_download_file_with_whitespace_url():
    """Test case 2: Test download_file function with whitespace-only URL raises ValueError."""
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        download_file("   ", "test.txt")


def test_download_file_with_none_url():
    """Test case 3: Test download_file function with None URL raises TypeError."""
    with pytest.raises(TypeError):
        download_file(None, "test.txt")


def test_download_file_with_empty_destination():
    """Test case 4: Test download_file function with empty destination raises ValueError."""
    with pytest.raises(ValueError, match="Destination must be a non-empty string"):
        download_file("https://example.com/file.txt", "")


def test_download_file_with_whitespace_destination():
    """Test case 5: Test download_file function with whitespace-only destination raises ValueError."""
    with pytest.raises(ValueError, match="Destination must be a non-empty string"):
        download_file("https://example.com/file.txt", "   ")


def test_download_file_with_none_destination():
    """Test case 6: Test download_file function with None destination raises TypeError."""
    with pytest.raises(TypeError):
        download_file("https://example.com/file.txt", None)


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_successful(mock_mkdir, mock_file_open, mock_urlopen):
    """Test case 7: Test successful file download returns correct response structure."""
    # Mock response
    mock_response = Mock()
    mock_response.headers = {"Content-Length": "1024"}
    mock_response.read.side_effect = [
        b"chunk1",
        b"chunk2",
        b"",
    ]  # Simulate chunked reading
    mock_urlopen.return_value.__enter__.return_value = mock_response

    # Mock Path.absolute() to return a predictable path
    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        result = download_file("https://example.com/file.txt", "/tmp/test.txt")

    assert result["success"] is True
    assert result["file_path"] == "/tmp/test.txt"
    assert result["file_size"] == 12  # len('chunk1') + len('chunk2')
    assert "Successfully downloaded 12 bytes" in result["message"]

    # Verify file was written
    mock_file_open.assert_called_once()
    handle = mock_file_open()
    assert handle.write.call_count == 2
    handle.write.assert_any_call(b"chunk1")
    handle.write.assert_any_call(b"chunk2")


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_with_custom_headers(mock_mkdir, mock_file_open, mock_urlopen):
    """Test case 8: Test file download with custom headers are properly set."""
    mock_response = Mock()
    mock_response.headers = {}
    mock_response.read.side_effect = [b"test", b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        headers = {"User-Agent": "TestAgent", "Authorization": "Bearer token"}
        download_file("https://example.com/file.txt", "/tmp/test.txt", headers=headers)

    # Verify headers were added to request
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    assert request.get_header("User-agent") == "TestAgent"
    assert request.get_header("Authorization") == "Bearer token"


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_with_progress_callback(mock_mkdir, mock_file_open, mock_urlopen):
    """Test case 9: Test file download with progress callback function called correctly."""
    mock_response = Mock()
    mock_response.headers = {"Content-Length": "100"}
    mock_response.read.side_effect = [b"a" * 50, b"b" * 50, b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    progress_calls = []

    def progress_callback(downloaded, total):
        progress_calls.append((downloaded, total))

    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        download_file(
            "https://example.com/file.txt",
            "/tmp/test.txt",
            progress_callback=progress_callback,
        )

    # Verify progress callback was called
    assert len(progress_calls) == 2
    assert progress_calls[0] == (50, 100)
    assert progress_calls[1] == (100, 100)


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_no_content_length_header(
    mock_mkdir, mock_file_open, mock_urlopen
):
    """Test case 10: Test file download when Content-Length header is missing."""
    mock_response = Mock()
    mock_response.headers = {}  # No Content-Length
    mock_response.read.side_effect = [b"test data", b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    progress_calls = []

    def progress_callback(downloaded, total):
        progress_calls.append((downloaded, total))

    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        result = download_file(
            "https://example.com/file.txt",
            "/tmp/test.txt",
            progress_callback=progress_callback,
        )

    assert result["success"] is True
    assert result["file_size"] == 9  # len('test data')

    # Progress callback should be called with total_size=0
    assert len(progress_calls) == 1
    assert progress_calls[0] == (9, 0)


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_with_custom_timeout(mock_mkdir, mock_file_open, mock_urlopen):
    """Test case 11: Test file download with custom timeout value."""
    mock_response = Mock()
    mock_response.headers = {}
    mock_response.read.side_effect = [b"test", b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        download_file("https://example.com/file.txt", "/tmp/test.txt", timeout=60)

    # Verify timeout was passed correctly
    mock_urlopen.assert_called_once()
    assert mock_urlopen.call_args[1]["timeout"] == 60


@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_download_file_default_timeout(mock_mkdir, mock_file_open, mock_urlopen):
    """Test case 12: Test that default timeout is 30 seconds when not specified."""
    mock_response = Mock()
    mock_response.headers = {}
    mock_response.read.side_effect = [b"test", b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("pathlib.Path.absolute") as mock_absolute:
        mock_absolute.return_value = Path("/tmp/test.txt")

        download_file("https://example.com/file.txt", "/tmp/test.txt")

        # Check that timeout=30 was passed
        assert mock_urlopen.call_args[1]["timeout"] == 30


@patch("urllib.request.urlopen")
@patch("pathlib.Path.unlink")
def test_download_file_request_failure(mock_unlink, mock_urlopen):
    """Test case 13: Test file download when request fails returns error response."""
    mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

    result = download_file("https://example.com/file.txt", "/tmp/test.txt")

    assert result["success"] is False
    assert result["file_size"] == 0
    assert "Download failed" in result["message"]
    assert "Connection failed" in result["message"]


@patch("urllib.request.urlopen")
@patch("builtins.open", side_effect=IOError("Write failed"))
@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.exists", return_value=True)
@patch("pathlib.Path.unlink")
def test_download_file_write_failure_cleanup(
    mock_unlink, mock_exists, mock_mkdir, mock_file_open, mock_urlopen
):
    """Test case 14: Test file download when file write fails performs cleanup."""
    mock_response = Mock()
    mock_response.headers = {}
    mock_response.read.side_effect = [b"test", b""]
    mock_urlopen.return_value.__enter__.return_value = mock_response

    result = download_file("https://example.com/file.txt", "/tmp/test.txt")

    assert result["success"] is False
    assert result["file_size"] == 0
    assert "Download failed" in result["message"]
    assert "Write failed" in result["message"]

    # Verify cleanup was attempted
    mock_unlink.assert_called_once()
