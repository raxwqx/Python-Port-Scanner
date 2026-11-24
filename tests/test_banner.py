"""portscan.banner için birim testleri."""

import socket

from portscan.banner import grab_banner


def test_grab_banner_reads_immediate_banner(banner_server):
    port = banner_server(
        lambda connection: connection.sendall(b"SSH-2.0-OpenSSH_9.6\r\n")
    )

    assert grab_banner("127.0.0.1", port, timeout=0.5) == "SSH-2.0-OpenSSH_9.6"


def test_grab_banner_probes_a_silent_service(banner_server):
    def handler(connection):
        connection.settimeout(1.0)
        try:
            request = connection.recv(1024)
        except socket.timeout:
            return
        if b"HEAD" in request:
            connection.sendall(b"HTTP/1.0 200 OK\r\n\r\n")

    port = banner_server(handler)

    assert grab_banner("127.0.0.1", port, timeout=0.5) == "HTTP/1.0 200 OK"


def test_grab_banner_returns_none_for_silent_service(banner_server):
    port = banner_server(lambda connection: None)

    assert grab_banner("127.0.0.1", port, timeout=0.2) is None


def test_grab_banner_returns_none_for_closed_port():
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()

    assert grab_banner("127.0.0.1", port, timeout=0.2) is None
