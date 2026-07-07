def format_mac(mac: str) -> str:
    raw = mac.replace("-", "").replace(":", "").upper()
    return ":".join(raw[i:i+2] for i in range(0, 12, 2))

def server_status_emoji(is_alive: bool) -> str:
    return "\U0001F7E2" if is_alive else "\U0001F534"

def server_status_text(is_alive: bool) -> str:
    return "ENCENDIDO" if is_alive else "APAGADO"
