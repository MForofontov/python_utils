"""Unit tests for file upload functionality."""

import pytest
from unittest.mock import patch, Mock, mock_open
from pathlib import Path
import urllib.error
from http_functions.upload_file import upload_file


def test_upload_file_with_empty_url():
    """
    Test upload_file function with empty URL raises ValueError.
    """
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        upload_file("", "test.txt")


def test_upload_file_with_whitespace_url():
    """
    Test upload_file function with whitespace-only URL raises ValueError.
    """
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        upload_file("   ", "test.txt")


def test_upload_file_with_none_url():
    """
    Test upload_file function with None URL raises TypeError.
    """
    with pytest.raises(TypeError):
        upload_file(None, "test.txt")


def test_upload_file_with_empty_file_path():
    """
    Test upload_file function with empty file path raises ValueError.
    """
    with pytest.raises(ValueError, match="file_path must be a non-empty string"):
        upload_file("https://example.com/upload", "")


def test_upload_file_with_whitespace_file_path():
    """
    Test upload_file function with whitespace-only file path raises ValueError.
    """
    with pytest.raises(ValueError, match="file_path must be a non-empty string"):
        upload_file("https://example.com/upload", "   ")


def test_upload_file_with_none_file_path():
    """
    Test upload_file function with None file path raises TypeError.
    """
    with pytest.raises(TypeError):
        upload_file("https://example.com/upload", None)


@patch('pathlib.Path.exists', return_value=False)
def test_upload_file_not_found(mock_exists):
    """
    Test upload_file function when file doesn't exist raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError, match="File not found"):
        upload_file("https://example.com/upload", "/tmp/nonexistent.txt")


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=False)
def test_upload_file_not_a_file(mock_is_file, mock_exists):
    """
    Test upload_file function when path is not a file raises ValueError.
    """
    with pytest.raises(ValueError, match="Path is not a file"):
        upload_file("https://example.com/upload", "/tmp/directory")


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test file content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_successful(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test successful file upload returns correct response structure.
    """
    # Mock response
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{"success": true}'
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    # Mock Path.name property
    with patch('pathlib.Path.name', 'test.txt'):
        result = upload_file('https://example.com/upload', '/tmp/test.txt')
    
    assert result['status_code'] == 200
    assert result['content'] == '{"success": true}'
    assert result['success'] is True
    
    # Verify request was made with multipart data
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    assert 'multipart/form-data' in request.get_header('Content-type')
    assert request.data is not None


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=(None, None))
def test_upload_file_unknown_content_type(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload when content type cannot be determined uses default.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    with patch('pathlib.Path.name', 'unknown_file'):
        upload_file('https://example.com/upload', '/tmp/unknown_file')
    
    # Verify default content type was used
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    body = request.data.decode('utf-8', errors='ignore')
    assert 'application/octet-stream' in body


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_with_custom_field_name(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload with custom field name parameter.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    with patch('pathlib.Path.name', 'test.txt'):
        upload_file('https://example.com/upload', '/tmp/test.txt', field_name='document')
    
    # Verify custom field name was used
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    body = request.data.decode('utf-8', errors='ignore')
    assert 'name="document"' in body


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_with_custom_headers(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload with additional custom headers.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    headers = {'Authorization': 'Bearer token', 'X-Custom': 'value'}
    
    with patch('pathlib.Path.name', 'test.txt'):
        upload_file('https://example.com/upload', '/tmp/test.txt', headers=headers)
    
    # Verify headers were added
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    assert request.get_header('Authorization') == 'Bearer token'
    assert request.get_header('X-custom') == 'value'


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_with_additional_data(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload with additional form data fields.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    additional_data = {'description': 'Test file', 'category': 'documents'}
    
    with patch('pathlib.Path.name', 'test.txt'):
        upload_file('https://example.com/upload', '/tmp/test.txt', additional_data=additional_data)
    
    # Verify additional data was included in multipart form
    call_args = mock_urlopen.call_args[0]
    request = call_args[0]
    body = request.data.decode('utf-8', errors='ignore')
    assert 'name="description"' in body
    assert 'Test file' in body
    assert 'name="category"' in body
    assert 'documents' in body


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_with_custom_timeout(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload with custom timeout value.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    with patch('pathlib.Path.name', 'test.txt'):
        upload_file('https://example.com/upload', '/tmp/test.txt', timeout=60)
    
    # Verify timeout was passed correctly
    mock_urlopen.assert_called_once()
    assert mock_urlopen.call_args[1]['timeout'] == 60


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_default_timeout(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test that default timeout is 30 seconds when not specified.
    """
    mock_response = Mock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'OK'
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    with patch('pathlib.Path.name', 'test.txt'):
        upload_file('https://example.com/upload', '/tmp/test.txt')
        
        # Check that timeout=30 was passed
        assert mock_urlopen.call_args[1]['timeout'] == 30


@patch('pathlib.Path.exists', return_value=True)
@patch('pathlib.Path.is_file', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=b'test content')
@patch('urllib.request.urlopen')
@patch('mimetypes.guess_type', return_value=('text/plain', None))
def test_upload_file_http_error(mock_guess_type, mock_urlopen, mock_file_open, mock_is_file, mock_exists):
    """
    Test file upload with HTTP error response returns error details.
    """
    error = urllib.error.HTTPError(
        url='https://example.com/upload',
        code=400,
        msg='Bad Request',
        hdrs={'Content-Type': 'application/json'},
        fp=Mock()
    )
    error.fp.read.return_value = b'{"error": "invalid file"}'
    mock_urlopen.side_effect = error
    
    with patch('pathlib.Path.name', 'test.txt'):
        result = upload_file('https://example.com/upload', '/tmp/test.txt')
    
    assert result['status_code'] == 400
    assert result['content'] == '{"error": "invalid file"}'
    assert result['success'] is False
    assert result['headers'] == {'Content-Type': 'application/json'}
