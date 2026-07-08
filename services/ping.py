import asyncio
import logging
import platform
import socket

logger = logging.getLogger(__name__)


async def ping_host(host: str, timeout: int = 3) -> bool:
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        process = await asyncio.create_subprocess_exec(
            "ping", param, "1", "-W", str(timeout), host,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout + 2)
            alive = process.returncode == 0
            logger.info("ping %s -> %s (rc=%s)", host, "alive" if alive else "dead", process.returncode)
            return alive
        except asyncio.TimeoutError:
            logger.warning("ping %s -> timeout after %ss", host, timeout + 2)
            process.kill()
            await process.wait()
            return False
    except FileNotFoundError:
        logger.error("ping: comando no encontrado. Instalar iputils-ping en el contenedor.")
        return False
    except Exception as e:
        logger.warning("ping %s -> error: %s", host, e)
        return False


async def check_port(host: str, port: int, timeout: int = 3) -> bool:
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, lambda: socket.create_connection((host, port), timeout=timeout).close()
        )
        logger.info("check_port %s:%s -> open", host, port)
        return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        logger.info("check_port %s:%s -> closed (%s)", host, port, e)
        return False
