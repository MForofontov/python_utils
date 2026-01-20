import base64
import json
from datetime import datetime, timezone

import pytest

try:
    from cryptography.fernet import Fernet
    from python_utils.security_functions.token_generation.generate_jwt_token import generate_jwt_token
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None  # type: ignore
    generate_jwt_token = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.security,
    pytest.mark.skipif(not CRYPTOGRAPHY_AVAILABLE, reason="cryptography not installed"),
]


def test_generate_jwt_token_basic_token() -> None:
    """
    Test case 1: Generate basic JWT token with simple payload.
    """
    # Arrange
    payload = {"user_id": 123, "username": "testuser"}
    secret = "my_secret_key"

    # Act
    token = generate_jwt_token(payload, secret)

    # Assert
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3  # header.payload.signature

    # Decode and verify payload
    encoded_payload = parts[1]
    # Add padding if necessary
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    assert decoded_payload["user_id"] == 123
    assert decoded_payload["username"] == "testuser"
    assert "iat" in decoded_payload
    assert "exp" in decoded_payload


def test_generate_jwt_token_custom_expiration() -> None:
    """
    Test case 2: Generate JWT token with custom expiration time.
    """
    # Arrange
    payload = {"data": "test"}
    secret = "secret_key"
    expires_in_hours = 2

    # Act
    token = generate_jwt_token(payload, secret, expires_in_hours)

    # Assert
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3

    # Verify expiration time
    encoded_payload = parts[1]
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    exp_time = decoded_payload["exp"]
    iat_time = decoded_payload["iat"]

    # Should be approximately 2 hours (7200 seconds) difference
    assert abs((exp_time - iat_time) - 7200) < 10  # Allow 10 second tolerance


def test_generate_jwt_token_complex_payload() -> None:
    """
    Test case 3: Generate JWT token with complex payload.
    """
    # Arrange
    payload = {
        "user_id": 456,
        "roles": ["admin", "user"],
        "permissions": {"read": True, "write": False},
        "metadata": {"login_count": 5},
    }
    secret = "complex_secret"

    # Act
    token = generate_jwt_token(payload, secret)

    # Assert
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3

    # Verify complex payload structure
    encoded_payload = parts[1]
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    assert decoded_payload["user_id"] == 456
    assert decoded_payload["roles"] == ["admin", "user"]
    assert decoded_payload["permissions"]["read"] is True
    assert decoded_payload["metadata"]["login_count"] == 5


def test_generate_jwt_token_header_verification() -> None:
    """
    Test case 4: Verify JWT header is correct.
    """
    # Arrange
    payload = {"test": "data"}
    secret = "test_secret"

    # Act
    token = generate_jwt_token(payload, secret)

    # Assert
    parts = token.split(".")
    encoded_header = parts[0]

    # Add padding if necessary
    padding = 4 - (len(encoded_header) % 4)
    if padding != 4:
        encoded_header += "=" * padding

    decoded_header = json.loads(base64.urlsafe_b64decode(encoded_header))
    assert decoded_header["alg"] == "HS256"
    assert decoded_header["typ"] == "JWT"


def test_generate_jwt_token_empty_payload() -> None:
    """
    Test case 5: Generate JWT token with empty payload.
    """
    # Arrange
    payload = {}
    secret = "secret_key"

    # Act
    token = generate_jwt_token(payload, secret)

    # Assert
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3

    # Verify empty payload still gets iat and exp
    encoded_payload = parts[1]
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    assert "iat" in decoded_payload
    assert "exp" in decoded_payload


def test_generate_jwt_token_different_secrets_different_signatures() -> None:
    """
    Test case 6: Different secrets should produce different signatures.
    """
    # Arrange
    payload = {"data": "same"}
    secret1 = "secret1"
    secret2 = "secret2"

    # Act
    token1 = generate_jwt_token(payload, secret1)
    token2 = generate_jwt_token(payload, secret2)

    # Assert
    parts1 = token1.split(".")
    parts2 = token2.split(".")

    # Header and payload should be the same (ignoring iat/exp differences)
    assert parts1[0] == parts2[0]  # Same header
    # Signatures should be different
    assert parts1[2] != parts2[2]


def test_generate_jwt_token_unicode_payload() -> None:
    """
    Test case 7: Handle Unicode characters in payload.
    """
    # Arrange
    payload = {
        "name": "José García",
        "message": "Hello 世界! 🌍",
        "unicode_key_🔑": "unicode_value_🎯",
    }
    secret = "unicode_secret"

    # Act
    token = generate_jwt_token(payload, secret)

    # Assert
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3

    # Verify Unicode content
    encoded_payload = parts[1]
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    assert decoded_payload["name"] == "José García"
    assert decoded_payload["message"] == "Hello 世界! 🌍"
    assert decoded_payload["unicode_key_🔑"] == "unicode_value_🎯"


def test_generate_jwt_token_timestamp_validation() -> None:
    """
    Test case 8: Verify iat and exp timestamps are reasonable.
    """
    # Arrange
    payload = {"test": "timestamps"}
    secret = "timestamp_secret"
    expires_in_hours = 1

    # Act
    before_time = datetime.now(timezone.utc).timestamp()
    token = generate_jwt_token(payload, secret, expires_in_hours)
    after_time = datetime.now(timezone.utc).timestamp()

    # Assert
    parts = token.split(".")
    encoded_payload = parts[1]
    padding = 4 - (len(encoded_payload) % 4)
    if padding != 4:
        encoded_payload += "=" * padding

    decoded_payload = json.loads(base64.urlsafe_b64decode(encoded_payload))
    iat = decoded_payload["iat"]
    exp = decoded_payload["exp"]

    # iat should be between before and after
    assert before_time <= iat <= after_time
    # exp should be approximately 1 hour after iat
    assert abs((exp - iat) - 3600) < 10  # Allow 10 second tolerance


def test_generate_jwt_token_type_validation() -> None:
    """
    Test case 9: Type validation for all parameters.
    """
    # Test invalid payload type
    with pytest.raises(TypeError, match="payload must be a dictionary"):
        generate_jwt_token("invalid", "secret")

    # Test invalid secret_key type
    with pytest.raises(TypeError, match="secret_key must be a string"):
        generate_jwt_token({}, 123)

    # Test invalid expires_in_hours type
    with pytest.raises(TypeError, match="expires_in_hours must be an integer"):
        generate_jwt_token({}, "secret", "invalid")


def test_generate_jwt_token_value_validation() -> None:
    """
    Test case 10: Value validation for parameters.
    """
    # Test empty secret_key
    with pytest.raises(ValueError, match="secret_key cannot be empty"):
        generate_jwt_token({"data": "test"}, "")

    # Test non-positive expires_in_hours
    with pytest.raises(ValueError, match="expires_in_hours must be positive"):
        generate_jwt_token({"data": "test"}, "secret", 0)

    with pytest.raises(ValueError, match="expires_in_hours must be positive"):
        generate_jwt_token({"data": "test"}, "secret", -1)
