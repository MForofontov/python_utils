from unittest.mock import MagicMock, patch

import pytest
from asyncio_functions.async_download import async_download


@pytest.mark.asyncio
async def test_async_download_normal_operation(tmp_path):
    """
    Test case 1: Normal operation with valid URL and destination.
    """
    url = "https://example.com/file.txt"
    dest = tmp_path / "file.txt"
    content = b"hello world"

    class MockResponse:
        def __init__(self):
            self.status = 200
            self.content = MagicMock()
            self.content.iter_chunked = self._iter_chunked

        async def _iter_chunked(self, size):
            yield content

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def raise_for_status(self):
            pass

    class MockSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, url):
            return MockResponse()

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        await async_download(url, str(dest))
        with open(dest, "rb") as f:
            assert f.read() == content


@pytest.mark.asyncio
async def test_async_download_type_error_url(tmp_path):
    """
    Test case 2: TypeError for non-string URL.
    """
    dest = tmp_path / "file.txt"
    with pytest.raises(TypeError, match="url must be str"):
        await async_download(123, str(dest))


@pytest.mark.asyncio
async def test_async_download_type_error_dest_path():
    """
    Test case 3: TypeError for non-string dest_path.
    """
    with pytest.raises(TypeError, match="dest_path must be str"):
        await async_download("https://example.com/file.txt", 123)


@pytest.mark.asyncio
async def test_async_download_value_error_url(tmp_path):
    """
    Test case 4: ValueError for empty URL.
    """
    dest = tmp_path / "file.txt"
    with pytest.raises(ValueError, match="url cannot be empty"):
        await async_download("", str(dest))


@pytest.mark.asyncio
async def test_async_download_type_error_timeout(tmp_path):
    """
    Test case 5: TypeError for invalid timeout type.
    """
    dest = tmp_path / "file.txt"
    with pytest.raises(TypeError, match="timeout must be a number"):
        await async_download("https://example.com/file.txt", str(dest), timeout="bad")


@pytest.mark.asyncio
async def test_async_download_value_error_timeout(tmp_path):
    """
    Test case 6: ValueError for non-positive timeout.
    """
    dest = tmp_path / "file.txt"
    with pytest.raises(ValueError, match="timeout must be positive"):
        await async_download("https://example.com/file.txt", str(dest), timeout=0)


@pytest.mark.asyncio
async def test_async_download_runtime_error(tmp_path):
    """
    Test case 7: RuntimeError for download failure.
    """
    url = "https://example.com/file.txt"
    dest = tmp_path / "file.txt"

    class MockSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, url):
            raise Exception("network error")

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        with pytest.raises(RuntimeError, match="Download failed: network error"):
            await async_download(url, str(dest))
