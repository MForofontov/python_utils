"""Unit tests for fetch_url function."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from asyncio_functions.fetch_url import fetch_url


@pytest.mark.asyncio
async def test_fetch_url_successful_fetch() -> None:
    """
    Test case 1: Successfully fetch content from a URL.
    """
    # Arrange
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="<html>Success</html>")
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    url = "https://example.com"

    # Act
    result = await fetch_url(mock_session, url)

    # Assert
    assert result == "<html>Success</html>"
    mock_session.get.assert_called_once_with(url)


@pytest.mark.asyncio
async def test_fetch_url_different_content() -> None:
    """
    Test case 2: Fetch different types of content.
    """
    # Arrange
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value='{"key": "value"}')
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    url = "https://api.example.com/data"

    # Act
    result = await fetch_url(mock_session, url)

    # Assert
    assert result == '{"key": "value"}'


@pytest.mark.asyncio
async def test_fetch_url_empty_response() -> None:
    """
    Test case 3: Fetch returns empty content.
    """
    # Arrange
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="")
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    url = "https://empty.example.com"

    # Act
    result = await fetch_url(mock_session, url)

    # Assert
    assert result == ""


@pytest.mark.asyncio
async def test_fetch_url_large_content() -> None:
    """
    Test case 4: Fetch large content.
    """
    # Arrange
    mock_session = MagicMock()
    large_content = "x" * 10000
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value=large_content)
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    url = "https://large.example.com"

    # Act
    result = await fetch_url(mock_session, url)

    # Assert
    assert len(result) == 10000
    assert result == large_content


@pytest.mark.asyncio
async def test_fetch_url_special_characters() -> None:
    """
    Test case 5: Content with special characters.
    """
    # Arrange
    mock_session = MagicMock()
    special_content = "Hello <>&\"' 世界"
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value=special_content)
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    url = "https://special.example.com"

    # Act
    result = await fetch_url(mock_session, url)

    # Assert
    assert result == special_content


@pytest.mark.asyncio
async def test_fetch_url_parameter_passed() -> None:
    """
    Test case 6: Verify URL parameter is correctly passed.
    """
    # Arrange
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="content")
    mock_session.get = MagicMock(return_value=mock_response)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    test_url = "https://test.example.com/path?param=value"

    # Act
    await fetch_url(mock_session, test_url)

    # Assert
    mock_session.get.assert_called_once_with(test_url)
