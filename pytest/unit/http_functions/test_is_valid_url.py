from http_functions.is_valid_url import is_valid_url


def test_is_valid_url_with_empty_string():
    """
    Test case 1: Test is_valid_url function with empty string returns False.
    """
    assert is_valid_url("") is False


def test_is_valid_url_with_whitespace_string():
    """
    Test case 2: Test is_valid_url function with whitespace-only string returns False.
    """
    assert is_valid_url("   ") is False


def test_is_valid_url_with_none():
    """
    Test case 3: Test is_valid_url function with None returns False.
    """
    assert is_valid_url(None) is False


def test_is_valid_url_with_integer():
    """
    Test case 4: Test is_valid_url function with integer returns False.
    """
    assert is_valid_url(123) is False


def test_is_valid_url_with_list():
    """
    Test case 5: Test is_valid_url function with list returns False.
    """
    assert is_valid_url([]) is False


def test_is_valid_url_simple_https():
    """
    Test case 6: Test is_valid_url function with simple HTTPS URL returns True.
    """
    assert is_valid_url("https://example.com") is True


def test_is_valid_url_simple_http():
    """
    Test case 7: Test is_valid_url function with simple HTTP URL returns True.
    """
    assert is_valid_url("http://example.com") is True


def test_is_valid_url_with_subdomain():
    """
    Test case 8: Is_valid_url function with subdomain returns True.
    """
    assert is_valid_url("https://www.example.com") is True


def test_is_valid_url_with_path():
    """
    Test case 9: Is_valid_url function with path returns True.
    """
    assert is_valid_url("https://example.com/path") is True


def test_is_valid_url_with_port():
    """
    Test case 10: Is_valid_url function with port returns True.
    """
    assert is_valid_url("https://example.com:8080") is True


def test_is_valid_url_with_query():
    """
    Test case 11: Is_valid_url function with query parameters returns True.
    """
    assert is_valid_url("https://example.com/path?query=value") is True


def test_is_valid_url_with_fragment():
    """
    Test case 12: Is_valid_url function with fragment returns True.
    """
    assert is_valid_url("https://example.com/path#fragment") is True


def test_is_valid_url_ftp_scheme():
    """
    Test case 13: Is_valid_url function with FTP scheme returns True.
    """
    assert is_valid_url("ftp://ftp.example.com") is True


def test_is_valid_url_file_scheme():
    """
    Test case 14: Is_valid_url function with file scheme returns True.
    """
    assert is_valid_url("file:///path/to/file") is True


def test_is_valid_url_with_authentication():
    """
    Test case 15: Is_valid_url function with authentication returns True.
    """
    assert is_valid_url("https://user:pass@example.com") is True


def test_is_valid_url_with_ip_address():
    """
    Test case 16: Is_valid_url function with IP address returns True.
    """
    assert is_valid_url("http://192.168.1.1:8000") is True


def test_is_valid_url_complex_subdomain():
    """
    Test case 17: Is_valid_url function with complex subdomain returns True.
    """
    assert is_valid_url("https://subdomain.example.com/api/v1") is True


def test_is_valid_url_no_scheme():
    """
    Test case 18: Is_valid_url function with no scheme returns False.
    """
    assert is_valid_url("example.com") is False


def test_is_valid_url_empty_scheme():
    """
    Test case 19: Is_valid_url function with empty scheme returns False.
    """
    assert is_valid_url("://example.com") is False


def test_is_valid_url_no_netloc():
    """
    Test case 20: Is_valid_url function with no netloc returns False.
    """
    assert is_valid_url("https://") is False


def test_is_valid_url_no_hostname():
    """
    Test case 21: Is_valid_url function with no hostname returns False.
    """
    assert is_valid_url("https:///path") is False


def test_is_valid_url_plain_text():
    """
    Test case 22: Is_valid_url function with plain text returns False.
    """
    assert is_valid_url("not-a-url") is False


def test_is_valid_url_just_text():
    """
    Test case 23: Is_valid_url function with just text returns False.
    """
    assert is_valid_url("just text") is False


def test_is_valid_url_www_without_scheme():
    """
    Test case 24: Is_valid_url function with www but no scheme returns False.
    """
    assert is_valid_url("www.example.com") is False


def test_is_valid_url_invalid_hostname():
    """
    Test case 25: Is_valid_url function with invalid hostname returns False.
    """
    assert is_valid_url("https://.example.com") is False


def test_is_valid_url_space_in_url():
    """
    Test case 26: Is_valid_url function with space in URL returns False.
    """
    assert is_valid_url("https:// example.com") is False


def test_is_valid_url_with_https_allowed_scheme():
    """
    Test case 27: Is_valid_url function with HTTPS in allowed schemes returns True.
    """
    assert is_valid_url("https://example.com", ["https"]) is True


def test_is_valid_url_with_http_not_in_allowed_schemes():
    """
    Test case 28: Is_valid_url function with HTTP not in allowed schemes returns False.
    """
    assert is_valid_url("http://example.com", ["https"]) is False


def test_is_valid_url_with_ftp_not_in_allowed_schemes():
    """
    Test case 29: Is_valid_url function with FTP not in allowed schemes returns False.
    """
    assert is_valid_url("ftp://example.com", ["https"]) is False


def test_is_valid_url_with_http_and_https_allowed():
    """
    Test case 30: Is_valid_url function with HTTP in allowed schemes returns True.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("http://example.com", allowed_schemes) is True


def test_is_valid_url_with_https_in_allowed_schemes():
    """
    Test case 31: Is_valid_url function with HTTPS in allowed schemes returns True.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("https://example.com", allowed_schemes) is True


def test_is_valid_url_with_ftp_not_in_http_https_schemes():
    """
    Test case 32: Is_valid_url function with FTP not in HTTP/HTTPS schemes returns False.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("ftp://example.com", allowed_schemes) is False


def test_is_valid_url_with_file_not_in_http_https_schemes():
    """
    Test case 33: Is_valid_url function with file not in HTTP/HTTPS schemes returns False.
    """
    allowed_schemes = ["http", "https"]
    assert is_valid_url("file:///path", allowed_schemes) is False


def test_is_valid_url_with_multiple_allowed_schemes():
    """
    Test case 34: Is_valid_url function with FTP in multiple allowed schemes returns True.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("ftp://ftp.example.com", allowed_schemes) is True


def test_is_valid_url_with_mailto_not_in_web_schemes():
    """
    Test case 35: Is_valid_url function with mailto not in web schemes returns False.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("mailto:test@example.com", allowed_schemes) is False


def test_is_valid_url_with_ssh_not_in_allowed_schemes():
    """
    Test case 36: Is_valid_url function with SSH not in allowed schemes returns False.
    """
    allowed_schemes = ["http", "https", "ftp"]
    assert is_valid_url("ssh://server.com", allowed_schemes) is False


def test_is_valid_url_with_empty_allowed_schemes():
    """
    Test case 37: Is_valid_url function with empty allowed schemes list returns False.
    """
    assert is_valid_url("https://example.com", []) is False


def test_is_valid_url_malformed_bracket():
    """
    Test case 38: Is_valid_url function with malformed bracket returns False.
    """
    assert is_valid_url("https://[invalid") is False


def test_is_valid_url_malformed_closing_bracket():
    """
    Test case 39: Is_valid_url function with malformed closing bracket returns False.
    """
    assert is_valid_url("https://]invalid") is False
