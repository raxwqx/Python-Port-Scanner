"""pytest ortak yapılandırması ve fixture'lar."""

import socket
import sys
import threading
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


@pytest.fixture
def udp_echo_port():
    """127.0.0.1 üzerinde gelen UDP paketini geri gönderen geçici sunucu."""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("127.0.0.1", 0))
    server.settimeout(0.2)
    port = server.getsockname()[1]
    stop = threading.Event()

    def echo():
        while not stop.is_set():
            try:
                data, address = server.recvfrom(1024)
            except socket.timeout:
                continue
            except OSError:
                break
            server.sendto(data or b"pong", address)

    thread = threading.Thread(target=echo, daemon=True)
    thread.start()
    try:
        yield port
    finally:
        stop.set()
        thread.join(timeout=1)
        server.close()


@pytest.fixture
def banner_server():
    """Her bağlantı için verilen handler'ı çalıştıran geçici TCP sunucusu."""
    servers = []

    def start(handler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(5)
        server.settimeout(0.1)
        port = server.getsockname()[1]
        stop = threading.Event()

        def loop():
            while not stop.is_set():
                try:
                    connection, _ = server.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                with connection:
                    try:
                        handler(connection)
                    except OSError:
                        pass

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
        servers.append((server, stop, thread))
        return port

    yield start

    for server, stop, thread in servers:
        stop.set()
        thread.join(timeout=1)
        server.close()
