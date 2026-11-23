"""pytest ortak yapılandırması ve fixture'lar."""

import socket
import sys
from pathlib import Path

import pytest

# Depo kökünü içe aktarma yoluna ekle (paket kurulmadan test çalışsın).
sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture
def listening_port():
    """127.0.0.1 üzerinde dinleyen geçici bir TCP portu döner."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen(5)
    port = server.getsockname()[1]
    try:
        yield port
    finally:
        server.close()
