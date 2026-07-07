import socket
from utils.helpers import format_mac

def _subnet_broadcast(ip: str) -> str | None:
    parts = ip.split(".")
    if len(parts) == 4:
        return ".".join(parts[:3] + ["255"])
    return None

def send_wol(mac: str, server_ip: str = "", port: int = 9) -> bool:
    try:
        mac_bytes = bytes.fromhex(format_mac(mac).replace(":", ""))
        if len(mac_bytes) != 6:
            return False

        magic_packet = b"\xff" * 6 + mac_bytes * 16

        addresses = ["255.255.255.255"]
        if server_ip:
            addresses.append(server_ip)
            subnet = _subnet_broadcast(server_ip)
            if subnet:
                addresses.append(subnet)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(2)
            for addr in set(addresses):
                sock.sendto(magic_packet, (addr, port))

        return True
    except Exception:
        return False
