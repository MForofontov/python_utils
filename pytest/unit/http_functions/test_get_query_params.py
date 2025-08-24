"""Unit tests for query parameters extraction functionality."""

import pytest
from http_functions.get_query_params import get_query_params


def test_get_query_params_with_empty_string():
    """
    Test get_query_params function with empty string raises ValueError.
    """
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        get_query_params("")


def test_get_query_params_with_whitespace_string():
    """
    Test get_query_params function with whitespace-only string raises ValueError.
    """
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        get_query_params("   ")


def test_get_query_params_with_none():
    """
    Test get_query_params function with None raises TypeError.
    """
    with pytest.raises(TypeError):
        get_query_params(None)


def test_get_query_params_no_query_simple_url():
    """
    Test get_query_params function with URL containing no query parameters.
    """
    url = "https://example.com"
    result = get_query_params(url)
    assert result == {}


def test_get_query_params_no_query_with_slash():
    """
    Test get_query_params function with URL ending in slash but no query.
    """
    url = "https://example.com/"
    result = get_query_params(url)
    assert result == {}


def test_get_query_params_no_query_with_path():
    """
    Test get_query_params function with URL containing path but no query.
    """
    url = "https://example.com/path"
    result = get_query_params(url)
    assert result == {}


def test_get_query_params_single_parameter():
    """
    Test get_query_params function with single query parameter.
    """
    url = "https://example.com?q=search"
    result = get_query_params(url)
    assert result == {'q': ['search']}


def test_get_query_params_single_parameter_with_path():
    """
    Test get_query_params function with single query parameter and path.
    """
    url = "https://example.com/path?page=1"
    result = get_query_params(url)
    assert result == {'page': ['1']}


def test_get_query_params_multiple_parameters():
    """
    Test get_query_params function with multiple query parameters.
    """
    url = "https://example.com?q=search&page=1&limit=10"
    result = get_query_params(url)
    
    expected = {
        'q': ['search'],
        'page': ['1'],
        'limit': ['10']
    }
    assert result == expected


def test_get_query_params_multiple_values_same_key():
    """
    Test get_query_params function with parameters having multiple values.
    """
    url = "https://example.com?tag=python&tag=web&tag=api"
    result = get_query_params(url)
    
    expected = {
        'tag': ['python', 'web', 'api']
    }
    assert result == expected


def test_get_query_params_mixed_single_and_multiple_values():
    """
    Test get_query_params function with mix of single and multiple value parameters.
    """
    url = "https://example.com?q=search&page=1&tag=python&tag=web&sort=date"
    result = get_query_params(url)
    
    expected = {
        'q': ['search'],
        'page': ['1'],
        'tag': ['python', 'web'],
        'sort': ['date']
    }
    assert result == expected


def test_get_query_params_empty_values():
    """
    Test get_query_params function with empty parameter values.
    """
    url = "https://example.com?q=&page=1&empty="
    result = get_query_params(url)
    
    expected = {
        'q': [''],
        'page': ['1'],
        'empty': ['']
    }
    assert result == expected


def test_get_query_params_parameters_without_values():
    """
    Test get_query_params function with parameters without values.
    """
    url = "https://example.com?debug&verbose&page=1"
    result = get_query_params(url)
    
    expected = {
        'debug': [''],
        'verbose': [''],
        'page': ['1']
    }
    assert result == expected


def test_get_query_params_url_encoded_values():
    """
    Test get_query_params function with URL-encoded values.
    """
    url = "https://example.com?q=hello%20world&message=caf%C3%A9"
    result = get_query_params(url)
    
    expected = {
        'q': ['hello world'],
        'message': ['café']
    }
    assert result == expected


def test_get_query_params_special_characters():
    """
    Test get_query_params function with special characters in values.
    """
    url = "https://example.com?symbols=%21%40%23%24&math=2%2B2%3D4"
    result = get_query_params(url)
    
    expected = {
        'symbols': ['!@#$'],
        'math': ['2+2=4']
    }
    assert result == expected


def test_get_query_params_with_fragment():
    """
    Test get_query_params function ignores URL fragment.
    """
    url = "https://example.com?q=search&page=1#section"
    result = get_query_params(url)
    
    expected = {
        'q': ['search'],
        'page': ['1']
    }
    assert result == expected


def test_get_query_params_with_port_and_path():
    """
    Test get_query_params function with port and path.
    """
    url = "https://example.com:8080/api/v1/search?q=test&limit=50"
    result = get_query_params(url)
    
    expected = {
        'q': ['test'],
        'limit': ['50']
    }
    assert result == expected


def test_get_query_params_complex_url():
    """
    Test get_query_params function with complex URL.
    """
    url = "https://user:pass@api.example.com:8080/v1/search?q=python&category=web&category=api&page=1&limit=20#results"
    result = get_query_params(url)
    
    expected = {
        'q': ['python'],
        'category': ['web', 'api'],
        'page': ['1'],
        'limit': ['20']
    }
    assert result == expected


def test_get_query_params_duplicate_parameters():
    """
    Test get_query_params function with duplicate parameters.
    """
    url = "https://example.com?filter=new&filter=popular&filter=trending"
    result = get_query_params(url)
    
    expected = {
        'filter': ['new', 'popular', 'trending']
    }
    assert result == expected


def test_get_query_params_plus_encoding():
    """
    Test get_query_params function with plus sign encoding for spaces.
    """
    url = "https://example.com?q=hello+world&phrase=search+term"
    result = get_query_params(url)
    
    expected = {
        'q': ['hello world'],
        'phrase': ['search term']
    }
    assert result == expected


def test_get_query_params_malformed_query():
    """
    Test get_query_params function with malformed query strings.
    """
    url = "https://example.com?key1value1&key2=value2"
    result = get_query_params(url)
    
    expected = {
        'key1value1': [''],
        'key2': ['value2']
    }
    assert result == expected


def test_get_query_params_only_query_separator():
    """
    Test get_query_params function with URL containing only query separator.
    """
    url = "https://example.com?"
    result = get_query_params(url)
    assert result == {}


def test_get_query_params_https_scheme():
    """
    Test get_query_params function works with HTTPS URLs.
    """
    url = "https://example.com?q=test"
    result = get_query_params(url)
    assert result == {'q': ['test']}


def test_get_query_params_http_scheme():
    """
    Test get_query_params function works with HTTP URLs.
    """
    url = "http://example.com?q=test"
    result = get_query_params(url)
    assert result == {'q': ['test']}


def test_get_query_params_ftp_scheme():
    """
    Test get_query_params function works with FTP URLs.
    """
    url = "ftp://ftp.example.com?mode=binary"
    result = get_query_params(url)
    assert result == {'mode': ['binary']}


def test_get_query_params_file_scheme():
    """
    Test get_query_params function works with file URLs.
    """
    url = "file:///path/to/file?param=value"
    result = get_query_params(url)
    assert result == {'param': ['value']}


def test_get_query_params_preserves_order():
    """
    Test get_query_params function preserves order of multiple values.
    """
    url = "https://example.com?priority=high&priority=medium&priority=low"
    result = get_query_params(url)
    
    # The order should be preserved
    assert result['priority'] == ['high', 'medium', 'low']
