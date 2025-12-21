"""
Tests for expand_url_template function.
"""

import pytest

from url_functions.expand_url_template import expand_url_template


def test_expand_url_template_simple_variable() -> None:
    """
    Test case 1: Simple variable substitution.
    """
    # Arrange
    template = "/users/{user_id}"
    variables = {"user_id": 123}
    expected = "/users/123"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_multiple_variables() -> None:
    """
    Test case 2: Multiple variable substitutions.
    """
    # Arrange
    template = "/users/{user_id}/posts/{post_id}"
    variables = {"user_id": 123, "post_id": 456}
    expected = "/users/123/posts/456"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_query_expansion() -> None:
    """
    Test case 3: Query string expansion with {?var}.
    """
    # Arrange
    template = "/search{?q,page}"
    variables = {"q": "python", "page": 2}
    expected = "/search?q=python&page=2"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_path_expansion() -> None:
    """
    Test case 4: Path segment expansion with {/var}.
    """
    # Arrange
    template = "/repos{/owner,repo}"
    variables = {"owner": "python", "repo": "cpython"}
    expected = "/repos/python/cpython"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_fragment_expansion() -> None:
    """
    Test case 5: Fragment expansion with {#var}.
    """
    # Arrange
    template = "/docs{#section}"
    variables = {"section": "installation"}
    expected = "/docs#installation"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_missing_variable_non_strict() -> None:
    """
    Test case 6: Missing variable with strict=False (default).
    """
    # Arrange
    template = "/users/{user_id}/posts/{post_id}"
    variables = {"user_id": 123}
    # Missing post_id should result in empty string for that part
    
    # Act
    result = expand_url_template(template, variables, strict=False)

    # Assert
    assert "/users/123/posts/" in result


def test_expand_url_template_missing_variable_strict_raises_error() -> None:
    """
    Test case 7: Missing variable with strict=True raises error.
    """
    # Arrange
    template = "/users/{user_id}/posts/{post_id}"
    variables = {"user_id": 123}
    expected_message = "Undefined variable: post_id"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        expand_url_template(template, variables, strict=True)


def test_expand_url_template_list_variable() -> None:
    """
    Test case 8: List variable in simple expansion.
    """
    # Arrange
    template = "/tags/{tags}"
    variables = {"tags": ["python", "web", "api"]}
    expected = "/tags/python,web,api"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_list_in_query() -> None:
    """
    Test case 9: List variable in query expansion.
    """
    # Arrange
    template = "/search{?tags}"
    variables = {"tags": ["python", "web"]}
    expected = "/search?tags=python&tags=web"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_url_encoding() -> None:
    """
    Test case 10: URL encoding of special characters.
    """
    # Arrange
    template = "/search{?q}"
    variables = {"q": "python & web"}
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert "python%20%26%20web" in result


def test_expand_url_template_empty_template_raises_error() -> None:
    """
    Test case 11: ValueError for empty template.
    """
    # Arrange
    template = ""
    variables = {"a": "1"}
    expected_message = "template cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        expand_url_template(template, variables)


def test_expand_url_template_invalid_template_type_raises_error() -> None:
    """
    Test case 12: TypeError for non-string template.
    """
    # Arrange
    template = 123
    variables = {"a": "1"}
    expected_message = "template must be a string, got int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        expand_url_template(template, variables)  # type: ignore


def test_expand_url_template_invalid_variables_type_raises_error() -> None:
    """
    Test case 13: TypeError for non-dict variables.
    """
    # Arrange
    template = "/users/{id}"
    variables = "invalid"
    expected_message = "variables must be a dict, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        expand_url_template(template, variables)  # type: ignore


def test_expand_url_template_no_variables() -> None:
    """
    Test case 14: Template without variables.
    """
    # Arrange
    template = "/api/v2/users"
    variables = {}
    expected = "/api/v2/users"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected


def test_expand_url_template_integer_variable() -> None:
    """
    Test case 15: Integer variable converted to string.
    """
    # Arrange
    template = "/page/{num}"
    variables = {"num": 42}
    expected = "/page/42"
    
    # Act
    result = expand_url_template(template, variables)

    # Assert
    assert result == expected
