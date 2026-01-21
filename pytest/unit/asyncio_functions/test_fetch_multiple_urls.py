from unittest.mock import AsyncMock, MagicMock, patch

import pytest

try:
    import aiohttp
    from pyutils_collection.asyncio_functions.fetch_multiple_urls import fetch_multiple_urls
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    aiohttp = None  # type: ignore
    fetch_multiple_urls = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.asyncio_functions,
    pytest.mark.skipif(not AIOHTTP_AVAILABLE, reason="aiohttp not installed"),
]


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_successful_fetch(
    mock_session_class: MagicMock,
) -> None:
    """
    Test case 1: Successfully fetch content from multiple URLs.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    # Mock responses for each URL
    mock_response1 = AsyncMock()
    mock_response1.text = AsyncMock(return_value="<html>Content 1</html>")
    mock_response1.__aenter__ = AsyncMock(return_value=mock_response1)
    mock_response1.__aexit__ = AsyncMock(return_value=None)

    mock_response2 = AsyncMock()
    mock_response2.text = AsyncMock(return_value="<html>Content 2</html>")
    mock_response2.__aenter__ = AsyncMock(return_value=mock_response2)
    mock_response2.__aexit__ = AsyncMock(return_value=None)

    mock_session.get = MagicMock(side_effect=[mock_response1, mock_response2])

    urls = ["https://example1.com", "https://example2.com"]

    # Act
    results = await fetch_multiple_urls(urls)

    # Assert
    assert results == ["<html>Content 1</html>", "<html>Content 2</html>"]
    assert mock_session.get.call_count == 2


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_empty_list(mock_session_class: MagicMock) -> None:
    """
    Test case 2: Empty URL list returns empty results.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    urls: list[str] = []

    # Act
    results = await fetch_multiple_urls(urls)

    # Assert
    assert results == []


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_single_url(mock_session_class: MagicMock) -> None:
    """
    Test case 3: Single URL in the list.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="Single content")
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session.get = MagicMock(return_value=mock_response)

    urls = ["https://single.com"]

    # Act
    results = await fetch_multiple_urls(urls)

    # Assert
    assert results == ["Single content"]


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_many_urls(mock_session_class: MagicMock) -> None:
    """
    Test case 4: Fetch from many URLs concurrently.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    responses = []
    for i in range(5):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(return_value=f"Content {i}")
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        responses.append(mock_response)

    mock_session.get = MagicMock(side_effect=responses)

    urls = [f"https://example{i}.com" for i in range(5)]

    # Act
    results = await fetch_multiple_urls(urls)

    # Assert
    assert len(results) == 5
    assert results == [f"Content {i}" for i in range(5)]


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_different_content_types(
    mock_session_class: MagicMock,
) -> None:
    """
    Test case 5: URLs return different content types.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    mock_response1 = AsyncMock()
    mock_response1.text = AsyncMock(return_value='{"json": "data"}')
    mock_response1.__aenter__ = AsyncMock(return_value=mock_response1)
    mock_response1.__aexit__ = AsyncMock(return_value=None)

    mock_response2 = AsyncMock()
    mock_response2.text = AsyncMock(return_value="<html>HTML content</html>")
    mock_response2.__aenter__ = AsyncMock(return_value=mock_response2)
    mock_response2.__aexit__ = AsyncMock(return_value=None)

    mock_session.get = MagicMock(side_effect=[mock_response1, mock_response2])

    urls = ["https://api.example.com", "https://web.example.com"]

    # Act
    results = await fetch_multiple_urls(urls)

    # Assert
    assert results == ['{"json": "data"}', "<html>HTML content</html>"]


@pytest.mark.asyncio
@patch("pyutils_collection.asyncio_functions.fetch_multiple_urls.aiohttp.ClientSession")
async def test_fetch_multiple_urls_session_created(
    mock_session_class: MagicMock,
) -> None:
    """
    Test case 6: Verify session is created and cleaned up.
    """
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value.__aenter__.return_value = mock_session
    mock_session_class.return_value.__aexit__.return_value = None

    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="content")
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session.get = MagicMock(return_value=mock_response)

    urls = ["https://test.com"]

    # Act
    await fetch_multiple_urls(urls)

    # Assert
    mock_session_class.assert_called_once()
    mock_session_class.return_value.__aenter__.assert_called_once()
    mock_session_class.return_value.__aexit__.assert_called_once()
