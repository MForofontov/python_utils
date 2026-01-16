import pytest
from testing_functions.test_data_generators.generate_random_url import (
    generate_random_url,
)


def test_generate_random_url_default_parameters() -> None:
    """
    Test case 1: Generate random URL with default parameters.
    """
    # Act
    result = generate_random_url()

    # Assert
    assert isinstance(result, str)
    assert result.startswith("https://example.com/")
    assert result.count("/") >= 3


def test_generate_random_url_custom_protocol() -> None:
    """
    Test case 2: Generate random URL with custom protocol.
    """
    # Act
    result = generate_random_url("http")

    # Assert
    assert result.startswith("http://")


def test_generate_random_url_custom_domain() -> None:
    """
    Test case 3: Generate random URL with custom domain.
    """
    # Act
    result = generate_random_url("https", "test.org")

    # Assert
    assert "test.org" in result


def test_generate_random_url_zero_path_length() -> None:
    """
    Test case 4: Generate random URL with zero path segments.
    """
    # Act
    result = generate_random_url("https", "example.com", 0)

    # Assert
    assert result == "https://example.com"


def test_generate_random_url_custom_path_length() -> None:
    """
    Test case 5: Generate random URL with custom path length.
    """
    # Act
    result = generate_random_url("https", "example.com", 5)

    # Assert
    path = result.replace("https://example.com/", "")
    assert path.count("/") == 4  # 5 segments means 4 slashes


def test_generate_random_url_type_error_protocol() -> None:
    """
    Test case 6: TypeError for invalid protocol type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="protocol must be a string"):
        generate_random_url(123)


def test_generate_random_url_type_error_domain() -> None:
    """
    Test case 7: TypeError for invalid domain type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="domain must be a string"):
        generate_random_url("https", 123)


def test_generate_random_url_type_error_path_length() -> None:
    """
    Test case 8: TypeError for invalid path_length type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="path_length must be an integer"):
        generate_random_url("https", "example.com", "3")


def test_generate_random_url_value_error_empty_protocol() -> None:
    """
    Test case 9: ValueError for empty protocol.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="protocol cannot be empty"):
        generate_random_url("")


def test_generate_random_url_value_error_empty_domain() -> None:
    """
    Test case 10: ValueError for empty domain.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="domain cannot be empty"):
        generate_random_url("https", "")


def test_generate_random_url_value_error_negative_path_length() -> None:
    """
    Test case 11: ValueError for negative path_length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="path_length must be non-negative"):
        generate_random_url("https", "example.com", -1)
