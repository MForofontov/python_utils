import subprocess
from typing import Any

def ssh_copy_file(
    local_path: str,
    remote_path: str,
    host: str,
    user: str | None = None,
    port: int = 22,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """
    Copy a local file to a remote host using SCP.

    Parameters
    ----------
    local_path : str
        Path to the local file to copy.
    remote_path : str
        Destination path on the remote host.
    host : str
        Hostname or IP address of the remote machine.
    user : str, optional
        SSH username (default: None, uses current user).
    port : int, optional
        SSH port (default: 22).
    timeout : float, optional
        Timeout in seconds (default: 30.0).

    Returns
    -------
    dict[str, Any]
        Dictionary with keys: 'stdout', 'stderr', 'exit_code'.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    RuntimeError
        If SCP command fails.

    Examples
    --------
    >>> ssh_copy_file('file.txt', '/tmp/file.txt', 'example.com')
    {'stdout': '', 'stderr': '', 'exit_code': 0}

    Notes
    -----
    Requires SSH access and `scp` command available.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(local_path, str):
        raise TypeError(f"local_path must be a string, got {type(local_path).__name__}")
    if not isinstance(remote_path, str):
        raise TypeError(f"remote_path must be a string, got {type(remote_path).__name__}")
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if user is not None and not isinstance(user, str):
        raise TypeError(f"user must be a string or None, got {type(user).__name__}")
    if not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    if not (1 <= port <= 65535):
        raise ValueError(f"port must be in 1-65535, got {port}")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError(f"timeout must be positive, got {timeout}")

    scp_target = f"{user + '@' if user else ''}{host}:{remote_path}"
    scp_cmd = [
        "scp",
        "-P", str(port),
        local_path,
        scp_target
    ]
    try:
        proc = subprocess.run(
            scp_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "exit_code": proc.returncode
        }
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"SCP command timed out after {timeout} seconds")
    except Exception as e:
        raise RuntimeError(f"SCP command failed: {e}")


__all__ = ['ssh_copy_file']
