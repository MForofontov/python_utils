from unittest.mock import patch

import pytest
from asyncio_functions.async_parallel_download import async_parallel_download


@pytest.mark.asyncio
async def test_async_parallel_download_normal_operation(tmp_path):
    """
    Test case 1: Normal operation with valid URL and destination.
    """
    url = "https://example.com/file.zip"
    dest = tmp_path / "file.zip"
    file_size = 16000
    num_chunks = 4
    chunk_data = b"x" * (file_size // num_chunks)
    last_chunk_data = b"y" * (file_size - (file_size // num_chunks) * (num_chunks - 1))

    class MockHeadResponse:
        def __init__(self):
            self.status = 200
            self.headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def raise_for_status(self):
            pass

    class MockGetResponse:
        def __init__(self, start, end):
            self.status = 206
            self._start = start
            self._end = end

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def raise_for_status(self):
            pass

        @property
        def content(self):
            class Content:
                async def read(inner_self):
                    if self._end < file_size - 1:
                        return chunk_data
                    else:
                        return last_chunk_data

            return Content()

    class MockSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def head(self, url):
            return MockHeadResponse()

        def get(self, url, headers=None):
            # Parse range
            rng = headers["Range"].split("=")[1]
            start, end = map(int, rng.split("-"))
            return MockGetResponse(start, end)

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        await async_parallel_download(url, str(dest), num_chunks=num_chunks)
        with open(dest, "rb") as f:
            data = f.read()
            assert data.count(b"x") == len(chunk_data) * (num_chunks - 1)
            assert data.endswith(last_chunk_data)


@pytest.mark.asyncio
async def test_async_parallel_download_more_chunks_than_size(tmp_path):
    """
    Ensure chunks are capped by file size so each chunk has at least one byte.
    """

    url = "https://example.com/small.bin"
    dest = tmp_path / "small.bin"
    file_size = 3
    num_chunks = 10

    class MockHeadResponse:
        def __init__(self):
            self.status = 200
            self.headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def raise_for_status(self):
            pass

    class MockGetResponse:
        def __init__(self, start, end, idx):
            self.status = 206
            self._start = start
            self._end = end
            self._idx = idx

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def raise_for_status(self):
            pass

        @property
        def content(self):
            class Content:
                def __init__(inner_self, idx, start, end):
                    inner_self._idx = idx
                    inner_self._start = start
                    inner_self._end = end

                async def read(inner_self):
                    length = inner_self._end - inner_self._start + 1
                    return bytes([65 + inner_self._idx]) * length

            return Content(self._idx, self._start, self._end)

    class MockSession:
        def __init__(self):
            self.requests = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def head(self, url):
            return MockHeadResponse()

        def get(self, url, headers=None):
            rng = headers["Range"].split("=")[1]
            start, end = map(int, rng.split("-"))
            idx = len(self.requests)
            self.requests.append((start, end))
            return MockGetResponse(start, end, idx)

    session = MockSession()
    with patch("aiohttp.ClientSession", return_value=session):
        await async_parallel_download(url, str(dest), num_chunks=num_chunks)

    assert len(session.requests) == file_size
    assert all(end - start == 0 for start, end in session.requests)

    with open(dest, "rb") as f:
        data = f.read()
    assert data == b"ABC"


@pytest.mark.asyncio
async def test_async_parallel_download_type_error_url(tmp_path):
    """
    Test case 2: TypeError for non-string URL.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(TypeError, match="url must be str"):
        await async_parallel_download(123, str(dest))


@pytest.mark.asyncio
async def test_async_parallel_download_type_error_dest_path():
    """
    Test case 3: TypeError for non-string dest_path.
    """
    with pytest.raises(TypeError, match="dest_path must be str"):
        await async_parallel_download("https://example.com/file.zip", 123)


@pytest.mark.asyncio
async def test_async_parallel_download_value_error_url(tmp_path):
    """
    Test case 4: ValueError for empty URL.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(ValueError, match="url cannot be empty"):
        await async_parallel_download("", str(dest))


@pytest.mark.asyncio
async def test_async_parallel_download_type_error_num_chunks(tmp_path):
    """
    Test case 5: TypeError for invalid num_chunks type.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(TypeError, match="num_chunks must be int"):
        await async_parallel_download(
            "https://example.com/file.zip", str(dest), num_chunks="bad"
        )


@pytest.mark.asyncio
async def test_async_parallel_download_value_error_num_chunks(tmp_path):
    """
    Test case 6: ValueError for num_chunks < 1.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(ValueError, match="num_chunks must be >= 1"):
        await async_parallel_download(
            "https://example.com/file.zip", str(dest), num_chunks=0
        )


@pytest.mark.asyncio
async def test_async_parallel_download_type_error_timeout(tmp_path):
    """
    Test case 7: TypeError for invalid timeout type.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(TypeError, match="timeout must be a number"):
        await async_parallel_download(
            "https://example.com/file.zip", str(dest), timeout="bad"
        )


@pytest.mark.asyncio
async def test_async_parallel_download_value_error_timeout(tmp_path):
    """
    Test case 8: ValueError for non-positive timeout.
    """
    dest = tmp_path / "file.zip"
    with pytest.raises(ValueError, match="timeout must be positive"):
        await async_parallel_download(
            "https://example.com/file.zip", str(dest), timeout=0
        )


@pytest.mark.asyncio
async def test_async_parallel_download_runtime_error_no_range(tmp_path):
    """
    Test case 9: RuntimeError if server does not support range requests.
    """
    url = "https://example.com/file.zip"
    dest = tmp_path / "file.zip"

    class MockHeadResponse:
        def __init__(self):
            self.status = 200
            self.headers = {"Content-Length": "1000", "Accept-Ranges": "none"}

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

        def head(self, url):
            return MockHeadResponse()

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        with pytest.raises(
            RuntimeError, match="Server does not support range requests"
        ):
            await async_parallel_download(url, str(dest))


@pytest.mark.asyncio
async def test_async_parallel_download_runtime_error_download(tmp_path):
    """
    Test case 10: RuntimeError for download failure.
    """
    url = "https://example.com/file.zip"
    dest = tmp_path / "file.zip"
    file_size = 1000
    num_chunks = 2

    class MockHeadResponse:
        def __init__(self):
            self.status = 200
            self.headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}

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

        def head(self, url):
            return MockHeadResponse()

        def get(self, url, headers=None):
            raise Exception("network error")

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        with pytest.raises(
            RuntimeError, match="Parallel download failed: network error"
        ):
            await async_parallel_download(url, str(dest), num_chunks=num_chunks)
