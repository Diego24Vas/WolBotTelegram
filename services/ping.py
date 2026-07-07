import subprocess
import platform
import socket

def ping_host(host: str, timeout: int = 3) -> bool:
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(
            ["ping", param, "1", "-W", str(timeout), host],
            capture_output=True,
            timeout=timeout + 2,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False

def check_port(host: str, port: int, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
