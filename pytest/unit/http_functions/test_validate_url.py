"""Unit tests for URL validation functionality."""

import pytest
from http_functions.validate_url import is_valid_url


def test_is_valid_url_with_empty_string():
    """
    Test is_valid_url function with empty string returns False.
    """
    assert is_valid_url("") is False


def test_is_valid_url_with_whitespace_string():
    """
    Test is_valid_url function with whitespace-only string returns False.
    """
    assert is_valid_url("   ") is False


def test_is_valid_url_with_none():
    """
    Test is_valid_url function with None returns False.
    """
    assert is_valid_url(None) is False


def test_is_valid_url_with_integer():
    """
    Test is_valid_url function with integer returns False.
    """
    assert is_valid_url(123) is False


def test_is_valid_url_with_list():
    """
    Test is_valid_url function with list returns False.
    """
    assert is_valid_url([]) is False


def test_is_valid_url_simple_https():
    """
    Test is_valid_url function with simple HTTPS URL returns True.
    """
    assert is_valid_url("https://example.com") is True


def test_is_valid_url_simple_http():
    """
    Test is_valid_url function with simple HTTP URL returns True.
    """
    assert is_valid_url("http://example.com") is True


def test_is_valid_url_with_subdomain():
    """
    Test is_valid_url function with subdomain returns True.
    """
    assert is_valid_url("https://www.example.com") is True


def test_is_valid_url_with_path():
    """
    Test is_valid_url function with path returns True.
    """
    assert is_valid_url("https://example.com/path") is True


def test_is_valid_url_with_port():
    """
    Test is_valid_url function with port returns True.
    """
    assert is_valid_url("https://example.com:8080") is True


def test_is_valid_url_with_query():
    """
    Test is_valid_url function with query parameters returns True.
    """
    assert is_valid_url("https://example.com/path?query=value") is True


def test_is_valid_url_with_fragment():
    """
    Test is_valid_url function with fragment returns True.
    """
    assert is_valid_url("https://example.com/path#fragment") is True


def test_is_valid_url_ftp_scheme():
    """
    Test is_valid_url function with FTP scheme returns True.
    """
    assert is_valid_url("ftp://ftp.example.com") is True


def test_is_valid_url_file_scheme():
    """
    Test is_valid_url function with file scheme returns True.
    """
    assert is_valid_url("file:///path/to/file") is True


def test_is_valid_url_with_authentication():
    """
    Test is_valid_url function with authentication returns True.
    """
    assert is_valid_url("https://user:pass@example.com") is True


def test_is_valid_url_with_ip_address():
    """
    Test is_valid_url function with IP address returns True.
    """
    assert is_valid_url("http://192.168.1.1:8000") is True


def test_is_valid_url_complex_subdomain():
    """
    Test is_valid_url function with complex subdomain returns True.
    """
    assert is_valid_url("https://subdomain.example.com/api/v1") is True


def test_is_valid_url_no_scheme():
    """
    Test is_valid_url function with no scheme returns False.
    """
    assert is_valid_url("example.com") is False


def test_is_valid_url_empty_scheme():
    """
    Test is_valid_url function with empty scheme returns False.
    """
    assert is_valid_url("://example.com") is False


def test_is_valid_url_no_netloc():
    """
    Test is_valid_url function with no netloc returns False.
    """
    assert is_valid_url("https://") is False


def test_is_valid_url_no_hostname():
    """
    Test is_valid_url function with no hostname returns False.
    """
    assert is_valid_url("https:///path") is False


def test_is_valid_url_plain_text():
    """
    Test is_valid_url function with plain text returns False.
    """
    assert is_valid_url("not-a-url") is False


def test_is_valid_url_just_text():
    """
    Test is_valid_url function with just text returns False.
    """
    assert is_valid_url("just text") is False


def test_is_valid_url_www_without_scheme():
    """
    Test is_valid_url function with www but no scheme returns False.
    """
    assert is_valid_url("www.example.com") is False


def test_is_valid_url_invalid_hostname():
    """
    Test is_valid_url function with invalid hostname returns False.
    """
    assert is_valid_url("https://.example.com") is False


def test_is_valid_url_space_in_url():
    """
    Test is_valid_url function with space in URL returns False.
    """
    assert is_valid_url("https:// example.com") is False


def test_is_valid_url_with_https_allowed_scheme():
    """
    Test is_valid_url function with HTTPS in allowed schemes returns True.
    """
    assert is_valid_url("https://example.com", ["https"]) is True


def test_is_valid_url_with_http_not_in_allowed_schemes():
    """
    Test is_valid_url function with HTTP not in allowed schemes returns False.
    """
    assert is_valid_url("http://example.com", ["https"]) is False


def test_is_valid_url_with_ftp_not_in_allowed_schemes():
    """
    Test is_valid_url function with FTP not in allowed schemes returns False.
    """
    assert is_valid_url("ftp://example.com", ["https"]) is False


def test_is_valid_url_with_http_and_https_allowed():
    """
    Test is_valid_url function with HTTP in allowed schemes returns True.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("http://example.com", allowed_schemes) is True


def test_is_valid_url_with_https_in_allowed_schemes():
    """
    Test is_valid_url function with HTTPS in allowed schemes returns True.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("https://example.com", allowed_schemes) is True


def test_is_valid_url_with_ftp_not_in_http_https_schemes():
    """
    Test is_valid_url function with FTP not in HTTP/HTTPS schemes returns False.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("ftp://example.com", allowed_schemes) is False


def test_is_valid_url_with_file_not_in_http_https_schemes():
    """
    Test is_valid_url function with file not in HTTP/HTTPS schemes returns False.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("file:///path", allowed_schemes) is False


def test_is_valid_url_with_multiple_allowed_schemes():
    """
    Test is_valid_url function with FTP in multiple allowed schemes returns True.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("ftp://ftp.example.com", allowed_schemes) is True


def test_is_valid_url_with_mailto_not_in_web_schemes():
    """
    Test is_valid_url function with mailto not in web schemes returns False.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("mailto:test@example.com", allowed_schemes) is False


def test_is_valid_url_with_ssh_not_in_allowed_schemes():
    """
    Test is_valid_url function with SSH not in allowed schemes returns False.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("ssh://server.com", allowed_schemes) is False


def test_is_valid_url_with_empty_allowed_schemes():
    """
    Test is_valid_url function with empty allowed schemes list returns False.
    """
    assert is_valid_url("https://example.com", []) is False


def test_is_valid_url_malformed_bracket():
    """
    Test is_valid_url function with malformed bracket returns False.
    """
    assert is_valid_url("https://[invalid") is False


def test_is_valid_url_malformed_closing_bracket():
    """
    Test is_valid_url function with malformed closing bracket returns False.
    """
    assert is_valid_url("https://]invalid") is False
