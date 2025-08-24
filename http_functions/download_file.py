"""File download functionality."""

import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import os


def download_file(url: str, destination: str, headers: Optional[Dict[str, str]] = None, 
                  timeout: int = 30, progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
    """
    Download a file from a URL to a local destination.
    
    Parameters
    ----------
    url : str
        The URL of the file to download.
    destination : str
        Local path where the file should be saved.
    headers : dict of str, optional
        HTTP headers to include in the request.
    timeout : int, optional
        Timeout in seconds (default: 30).
    progress_callback : callable, optional
        Function to call with (downloaded_bytes, total_bytes) for progress tracking.
        
    Returns
    -------
    dict
        Dictionary containing 'success', 'file_path', 'file_size', and 'message'.
        
    Raises
    ------
    ValueError
        If URL or destination is invalid.
    urllib.error.URLError
        If the download fails.
        
    Examples
    --------
    >>> result = download_file('https://httpbin.org/image/png', 'test.png')
    >>> result['success']
    True
    >>> os.path.exists(result['file_path'])
    True
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    if not isinstance(destination, str) or not destination.strip():
        raise ValueError("Destination must be a non-empty string")
    
    # Create destination directory if it doesn't exist
    dest_path = Path(destination)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create request
    req = urllib.request.Request(url)
    
    # Add headers if provided
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # Get content length if available
            content_length = response.headers.get('Content-Length')
            total_size = int(content_length) if content_length else 0
            
            downloaded = 0
            chunk_size = 8192
            
            with open(dest_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(downloaded, total_size)
            
            return {
                'success': True,
                'file_path': str(dest_path.absolute()),
                'file_size': downloaded,
                'message': f"Successfully downloaded {downloaded} bytes"
            }
            
    except Exception as e:
        # Clean up partial file if it exists
        if dest_path.exists():
            dest_path.unlink()
        
        return {
            'success': False,
            'file_path': str(dest_path.absolute()),
            'file_size': 0,
            'message': f"Download failed: {str(e)}"
        }
