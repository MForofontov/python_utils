"""Unit tests for URL building functionality."""

import pytest
from http_functions.build_url import build_url


def test_build_url_with_empty_scheme():
    """Test case 1: Test build_url function with empty scheme raises ValueError."""
    with pytest.raises(ValueError, match="Scheme must be a non-empty string"):
        build_url("", "example.com")


def test_build_url_with_whitespace_scheme():
    """Test case 2: Test build_url function with whitespace-only scheme raises ValueError."""
    with pytest.raises(ValueError, match="Scheme must be a non-empty string"):
        build_url("   ", "example.com")


def test_build_url_with_none_scheme():
    """Test case 3: Test build_url function with None scheme raises TypeError."""
    with pytest.raises(TypeError):
        build_url(None, "example.com")


def test_build_url_with_empty_hostname():
    """Test case 4: Test build_url function with empty hostname raises ValueError."""
    with pytest.raises(ValueError, match="Hostname must be a non-empty string"):
        build_url("https", "")


def test_build_url_with_whitespace_hostname():
    """Test case 5: Test build_url function with whitespace-only hostname raises ValueError."""
    with pytest.raises(ValueError, match="Hostname must be a non-empty string"):
        build_url("https", "   ")


def test_build_url_with_none_hostname():
    """Test case 6: Test build_url function with None hostname raises TypeError."""
    with pytest.raises(TypeError):
        build_url("https", None)


def test_build_url_simple():
    """Test case 7: Test build_url function with basic scheme and hostname."""
    result = build_url('https', 'example.com')
    assert result == 'https://example.com'


def test_build_url_with_path():
    """Test case 8: Test build_url function with path component."""
    result = build_url('https', 'example.com', path='/api/v1')
    assert result == 'https://example.com/api/v1'


def test_build_url_with_port():
    """Test case 9: Test build_url function with port number."""
    result = build_url('https', 'example.com', port=8080)
    assert result == 'https://example.com:8080'


def test_build_url_with_port_and_path():
    """Test case 10: Test build_url function with both port and path."""
    result = build_url('https', 'example.com', port=8080, path='/api')
    assert result == 'https://example.com:8080/api'


def test_build_url_with_single_query_param():
    """Test case 11: Test build_url function with single query parameter."""
    result = build_url('https', 'example.com', query_params={'q': 'search'})
    assert result == 'https://example.com?q=search'


def test_build_url_with_multiple_query_params():
    """Test case 12: Test build_url function with multiple query parameters."""
    query_params = {'q': 'search', 'page': '1'}
    result = build_url('https', 'example.com', query_params=query_params)
    assert 'q=search' in result
    assert 'page=1' in result
    assert result.startswith('https://example.com?')


def test_build_url_with_fragment():
    """Test case 13: Test build_url function with fragment component."""
    result = build_url('https', 'example.com', fragment='section1')
    assert result == 'https://example.com#section1'


def test_build_url_with_username():
    """Test case 14: Test build_url function with username only."""
    result = build_url('https', 'example.com', username='user')
    assert result == 'https://user@example.com'


def test_build_url_with_username_and_password():
    """Test case 15: Test build_url function with username and password."""
    result = build_url('https', 'example.com', username='user', password='pass')
    assert result == 'https://user:pass@example.com'


def test_build_url_complex_all_components():
    """Test case 16: Test build_url function with all components present."""
    query_params = {'limit': '10', 'offset': '20'}
    result = build_url(
        scheme='https',
        hostname='example.com',
        port=8080,
        path='/api/v1/users',
        query_params=query_params,
        fragment='results',
        username='user',
        password='pass'
    )
    
    assert result.startswith('https://user:pass@example.com:8080/api/v1/users?')
    assert result.endswith('#results')
    assert 'limit=10' in result
    assert 'offset=20' in result


def test_build_url_http_scheme():
    """Test case 17: Test build_url function with HTTP scheme."""
    result = build_url('http', 'example.com')
    assert result == 'http://example.com'


def test_build_url_with_ip_address():
    """Test case 18: Test build_url function with IP address as hostname."""
    result = build_url('http', '192.168.1.1', port=8000)
    assert result == 'http://192.168.1.1:8000'


def test_build_url_with_subdomain():
    """Test case 19: Test build_url function with subdomain hostname."""
    result = build_url('https', 'api.example.com', path='/v1')
    assert result == 'https://api.example.com/v1'


def test_build_url_empty_path():
    """Test case 20: Test build_url function with empty path string."""
    result = build_url('https', 'example.com', path='')
    assert result == 'https://example.com'


def test_build_url_empty_query_params():
    """Test case 21: Test build_url function with empty query parameters dict."""
    result = build_url('https', 'example.com', query_params={})
    assert result == 'https://example.com'


def test_build_url_none_query_params():
    """Test case 22: Test build_url function with None query parameters."""
    result = build_url('https', 'example.com', query_params=None)
    assert result == 'https://example.com'


def test_build_url_none_fragment():
    """Test case 23: Test build_url function with None fragment."""
    result = build_url('https', 'example.com', fragment=None)
    assert result == 'https://example.com'


def test_build_url_empty_fragment():
    """Test case 24: Test build_url function with empty fragment string."""
    result = build_url('https', 'example.com', fragment='')
    assert result == 'https://example.com'


def test_build_url_special_characters_in_query():
    """Test case 25: Test build_url function properly encodes special characters in query params."""
    query_params = {'q': 'hello world', 'symbols': '!@#$'}
    result = build_url('https', 'example.com', query_params=query_params)
    
    assert 'hello+world' in result or 'hello%20world' in result
    assert '%21%40%23%24' in result or '!@#$' in result
