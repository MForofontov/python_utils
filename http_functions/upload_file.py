"""File upload functionality."""

import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from pathlib import Path
from typing import Any
import mimetypes
import uuid


def upload_file(
    url: str,
    file_path: str,
    field_name: str = "file",
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    additional_data: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Upload a file using multipart/form-data encoding.

    Parameters
    ----------
    url : str
        The URL to upload the file to.
    file_path : str
        Path to the file to upload.
    field_name : str, optional
        Name of the form field for the file (default: "file").
    headers : dict of str, optional
        Additional HTTP headers to include in the request.
    timeout : int, optional
        Timeout in seconds (default: 30).
    additional_data : dict of str, optional
        Additional form data to include in the upload.

    Returns
    -------
    dict
        Dictionary containing 'status_code', 'content', 'headers', and 'success'.

    Raises
    ------
    ValueError
        If URL or file_path is invalid.
    FileNotFoundError
        If the file doesn't exist.

    Examples
    --------
    >>> with open('test.txt', 'w') as f:
    ...     f.write('test content')
    >>> result = upload_file('https://httpbin.org/post', 'test.txt')
    >>> result['success']
    True
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("file_path must be a non-empty string")

    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path_obj.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Generate boundary for multipart data
    boundary = uuid.uuid4().hex

    # Guess content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"

    # Build multipart data
    data_parts = []

    # Add additional form data if provided
    if additional_data:
        for key, value in additional_data.items():
            data_parts.append(f"--{boundary}")
            data_parts.append(f'Content-Disposition: form-data; name="{key}"')
            data_parts.append("")
            data_parts.append(value)

    # Add file data
    data_parts.append(f"--{boundary}")
    data_parts.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path_obj.name}"'
    )
    data_parts.append(f"Content-Type: {content_type}")
    data_parts.append("")

    # Join text parts
    body_start = "\r\n".join(data_parts) + "\r\n"
    body_end = f"\r\n--{boundary}--\r\n"

    # Read file content
    with open(file_path_obj, "rb") as f:
        file_content = f.read()

    # Combine all parts
    body = body_start.encode("utf-8") + file_content + body_end.encode("utf-8")

    # Create request
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body)))

    # Add additional headers if provided
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8")
            return {
                "status_code": response.getcode(),
                "content": content,
                "headers": dict(response.headers),
                "success": True,
            }
    except HTTPError as e:
        return {
            "status_code": e.code,
            "content": e.read().decode("utf-8") if e.fp else "",
            "headers": dict(e.headers) if e.headers else {},
            "success": False,
        }
    except URLError as e:
        return {
            "status_code": None,
            "content": str(e.reason),
            "headers": {},
            "success": False,
        }
