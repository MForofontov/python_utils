import pytest
from testing_functions.mock_helpers.mock_api_response import mock_api_response


def test_mock_api_response_case_1_default_parameters() -> None:
    """
    Test case 1: Create mock API response with defaults.
    """
    # Act
    response = mock_api_response()
    
    # Assert
    assert response.status_code == 200
    assert response.headers == {}
    assert response.json() is None


def test_mock_api_response_case_2_custom_status_code() -> None:
    """
    Test case 2: Create mock with custom status code.
    """
    # Act
    response = mock_api_response(404)
    
    # Assert
    assert response.status_code == 404


def test_mock_api_response_case_3_with_data() -> None:
    """
    Test case 3: Create mock with JSON data.
    """
    # Arrange
    data = {"key": "value", "count": 42}
    
    # Act
    response = mock_api_response(200, data)
    
    # Assert
    assert response.json() == data
    assert "key" in response.json()


def test_mock_api_response_case_4_with_headers() -> None:
    """
    Test case 4: Create mock with custom headers.
    """
    # Arrange
    headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}
    
    # Act
    response = mock_api_response(200, None, headers)
    
    # Assert
    assert response.headers == headers


def test_mock_api_response_case_5_text_attribute() -> None:
    """
    Test case 5: Verify text attribute.
    """
    # Arrange
    data = {"message": "Hello"}
    
    # Act
    response = mock_api_response(200, data)
    
    # Assert
    assert "message" in response.text


def test_mock_api_response_case_6_error_status_codes() -> None:
    """
    Test case 6: Create mock with various error codes.
    """
    # Act
    response_400 = mock_api_response(400)
    response_500 = mock_api_response(500)
    
    # Assert
    assert response_400.status_code == 400
    assert response_500.status_code == 500


def test_mock_api_response_case_7_type_error_status_code() -> None:
    """
    Test case 7: TypeError for invalid status_code type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="status_code must be an integer"):
        mock_api_response("200")


def test_mock_api_response_case_8_type_error_headers() -> None:
    """
    Test case 8: TypeError for invalid headers type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="headers must be a dict or None"):
        mock_api_response(200, None, "headers")


def test_mock_api_response_case_9_value_error_invalid_status_code() -> None:
    """
    Test case 9: ValueError for invalid status code.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="status_code must be between 100 and 599"):
        mock_api_response(99)


def test_mock_api_response_case_10_value_error_status_code_too_high() -> None:
    """
    Test case 10: ValueError for status code too high.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="status_code must be between 100 and 599"):
        mock_api_response(600)
