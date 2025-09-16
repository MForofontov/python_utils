"""
Unit tests for verify_jwt_token function.
"""

import base64
import json
from datetime import datetime, timedelta, timezone

import pytest
from security_functions.token_generation.generate_jwt_token import generate_jwt_token
from security_functions.token_generation.verify_jwt_token import verify_jwt_token


def test_verify_jwt_token_case_1_valid_token() -> None:
    """
    Test case 1: Verify valid JWT token returns correct payload.
    """
    # Arrange
    payload = {"user_id": 123, "username": "testuser"}
    secret = "my_secret_key"
    token = generate_jwt_token(payload, secret)

    # Act
    decoded_payload = verify_jwt_token(token, secret)

    # Assert
    assert decoded_payload["user_id"] == 123
    assert decoded_payload["username"] == "testuser"
    assert "iat" in decoded_payload
    assert "exp" in decoded_payload


def test_verify_jwt_token_case_2_wrong_secret() -> None:
    """
    Test case 2: Wrong secret should raise ValueError.
    """
    # Arrange
    payload = {"user_id": 123}
    correct_secret = "correct_secret"
    wrong_secret = "wrong_secret"
    token = generate_jwt_token(payload, correct_secret)

    # Act & Assert
    with pytest.raises(ValueError, match="invalid token signature"):
        verify_jwt_token(token, wrong_secret)


def test_verify_jwt_token_case_3_malformed_token() -> None:
    """
    Test case 3: Malformed token should raise ValueError.
    """
    # Test token with wrong number of parts
    with pytest.raises(ValueError, match="invalid JWT format"):
        verify_jwt_token("invalid.token", "secret")

    # Test token with only one part
    with pytest.raises(ValueError, match="invalid JWT format"):
        verify_jwt_token("onlyonepart", "secret")

    # Test token with too many parts
    with pytest.raises(ValueError, match="invalid JWT format"):
        verify_jwt_token("too.many.parts.here", "secret")


def test_verify_jwt_token_case_4_type_validation() -> None:
    """
    Test case 4: Type validation for all parameters.
    """
    token = generate_jwt_token({"test": "data"}, "secret")

    # Test invalid token type
    with pytest.raises(TypeError, match="token must be a string"):
        verify_jwt_token(123, "secret")

    # Test invalid secret_key type
    with pytest.raises(TypeError, match="secret_key must be a string"):
        verify_jwt_token(token, 123)


def test_verify_jwt_token_case_5_value_validation() -> None:
    """
    Test case 5: Value validation for parameters.
    """
    # Test empty token
    with pytest.raises(ValueError, match="token cannot be empty"):
        verify_jwt_token("", "secret")

    # Test empty secret_key
    valid_token = generate_jwt_token({"test": "data"}, "secret")
    with pytest.raises(ValueError, match="secret_key cannot be empty"):
        verify_jwt_token(valid_token, "")


def test_verify_jwt_token_case_6_invalid_base64() -> None:
    """
    Test case 6: Invalid base64 encoding should raise ValueError.
    """
    # Create token with invalid base64
    invalid_token = "invalid_base64.invalid_base64.invalid_base64"

    # Act & Assert
    with pytest.raises(ValueError, match="invalid base64url encoding"):
        verify_jwt_token(invalid_token, "secret")


def test_verify_jwt_token_case_7_invalid_json() -> None:
    """
    Test case 7: Invalid JSON in token should raise ValueError.
    """
    # Create token with invalid JSON (but valid base64)
    invalid_json = base64.urlsafe_b64encode(b"not_json").decode("utf-8").rstrip("=")
    invalid_token = f"{invalid_json}.{invalid_json}.{invalid_json}"

    # Act & Assert
    with pytest.raises(ValueError, match="invalid JSON in token"):
        verify_jwt_token(invalid_token, "secret")


def test_verify_jwt_token_case_8_unsupported_algorithm() -> None:
    """
    Test case 8: Unsupported algorithm should raise ValueError.
    """
    # Create token with different algorithm manually
    header = {"alg": "RS256", "typ": "JWT"}  # Different algorithm
    payload = {"test": "data"}

    def encode_part(data):
        json_str = json.dumps(data, separators=(",", ":"))
        encoded = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        return encoded.decode("utf-8").rstrip("=")

    encoded_header = encode_part(header)
    encoded_payload = encode_part(payload)
    fake_signature = "fake_signature"

    invalid_token = f"{encoded_header}.{encoded_payload}.{fake_signature}"

    # Act & Assert
    with pytest.raises(ValueError, match="unsupported algorithm"):
        verify_jwt_token(invalid_token, "secret")


def test_verify_jwt_token_case_9_expired_token() -> None:
    """
    Test case 9: Expired token should raise ValueError.
    """
    # Create an expired token manually
    header = {"alg": "HS256", "typ": "JWT"}
    past_time = datetime.now(timezone.utc) - timedelta(hours=2)
    payload = {
        "test": "data",
        "iat": int(past_time.timestamp()),
        "exp": int((past_time + timedelta(hours=1)).timestamp()),  # Expired 1 hour ago
    }

    def encode_part(data):
        json_str = json.dumps(data, separators=(",", ":"))
        encoded = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        return encoded.decode("utf-8").rstrip("=")

    encoded_header = encode_part(header)
    encoded_payload = encode_part(payload)

    # Create proper signature
    import hashlib
    import hmac

    message = f"{encoded_header}.{encoded_payload}"
    secret = "test_secret"
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    expired_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    # Act & Assert
    with pytest.raises(ValueError, match="token has expired"):
        verify_jwt_token(expired_token, secret)


def test_verify_jwt_token_case_10_invalid_expiration_format() -> None:
    """
    Test case 10: Invalid expiration time format should raise ValueError.
    """
    # Create token with invalid exp format manually
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"test": "data", "exp": "not_a_timestamp"}  # Invalid format

    def encode_part(data):
        json_str = json.dumps(data, separators=(",", ":"))
        encoded = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        return encoded.decode("utf-8").rstrip("=")

    encoded_header = encode_part(header)
    encoded_payload = encode_part(payload)

    # Create proper signature
    import hashlib
    import hmac

    message = f"{encoded_header}.{encoded_payload}"
    secret = "test_secret"
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    invalid_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    # Act & Assert
    with pytest.raises(ValueError, match="invalid expiration time format"):
        verify_jwt_token(invalid_token, secret)


def test_verify_jwt_token_case_11_complex_payload() -> None:
    """
    Test case 11: Verify token with complex payload structure.
    """
    # Arrange
    payload = {
        "user_id": 456,
        "roles": ["admin", "user"],
        "permissions": {"read": True, "write": False},
        "metadata": {"login_count": 5},
    }
    secret = "complex_secret"
    token = generate_jwt_token(payload, secret)

    # Act
    decoded_payload = verify_jwt_token(token, secret)

    # Assert
    assert decoded_payload["user_id"] == 456
    assert decoded_payload["roles"] == ["admin", "user"]
    assert decoded_payload["permissions"]["read"] is True
    assert decoded_payload["metadata"]["login_count"] == 5


def test_verify_jwt_token_case_12_token_without_expiration() -> None:
    """
    Test case 12: Token without expiration should verify successfully.
    """
    # Create token without exp claim manually
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "test": "data",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        # No exp claim
    }

    def encode_part(data):
        json_str = json.dumps(data, separators=(",", ":"))
        encoded = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        return encoded.decode("utf-8").rstrip("=")

    encoded_header = encode_part(header)
    encoded_payload = encode_part(payload)

    # Create proper signature
    import hashlib
    import hmac

    message = f"{encoded_header}.{encoded_payload}"
    secret = "test_secret"
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    token_no_exp = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    # Act
    decoded_payload = verify_jwt_token(token_no_exp, secret)

    # Assert
    assert decoded_payload["test"] == "data"
    assert "exp" not in decoded_payload
