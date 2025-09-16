import subprocess
from typing import Any


def ssh_check_connection(
    host: str,
    user: str | None = None,
    port: int = 22,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """
    Check SSH connectivity to a remote host.

    Parameters
    ----------
    host : str
        Hostname or IP address of the remote machine.
    user : str, optional
        SSH username (default: None, uses current user).
    port : int, optional
        SSH port (default: 22).
    timeout : float, optional
        Timeout in seconds (default: 10.0).

    Returns
    -------
    dict[str, Any]
        Dictionary with keys: 'success', 'stdout', 'stderr', 'exit_code'.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    RuntimeError
        If SSH connection fails.

    Examples
    --------
    >>> ssh_check_connection('example.com')
    {'success': True, 'stdout': '', 'stderr': '', 'exit_code': 0}

    Notes
    -----
    Uses SSH with a simple 'exit' command to test connectivity.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
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

    ssh_target = f"{user + '@' if user else ''}{host}"
    ssh_cmd = ["ssh", "-p", str(port), ssh_target, "exit"]
    try:
        proc = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"SSH connection timed out after {timeout} seconds"
        ) from exc
    except Exception as exc:
        raise RuntimeError(f"SSH connection failed: {exc}") from exc


__all__ = ["ssh_check_connection"]
