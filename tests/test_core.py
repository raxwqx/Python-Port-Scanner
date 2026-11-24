"""portscan.core için birim testleri."""

import socket

import pytest

from portscan.core import (
    parse_ports,
    resolve_target,
    scan_port,
    scan_ports,
    scan_udp_port,
    scan_udp_ports,
)


def test_parse_single_port():
    assert parse_ports("80") == [80]


def test_parse_range():
    assert parse_ports("20-25") == [20, 21, 22, 23, 24, 25]


def test_parse_mixed_list_is_sorted_and_unique():
    assert parse_ports("443,80,80,100-102") == [80, 100, 101, 102, 443]


def test_parse_ignores_blank_items():
    assert parse_ports(" 22, ,80 ") == [22, 80]


@pytest.mark.parametrize(
    "spec",
    ["0", "65536", "10-5", "abc", "22-", "1-", "-5", "1-abc"],
)
def test_parse_rejects_invalid(spec):
    with pytest.raises(ValueError):
        parse_ports(spec)


def test_resolve_target_localhost():
    assert resolve_target("localhost").startswith("127.")


def test_resolve_target_invalid():
    with pytest.raises(ValueError):
        resolve_target("bu-hedef-gecersiz.invalid")


def test_scan_port_detects_open_port(listening_port):
    assert scan_port("127.0.0.1", listening_port, timeout=1.0) is True


def test_scan_ports_returns_open_ports(listening_port):
    assert scan_ports("127.0.0.1", [listening_port], timeout=1.0, workers=4) == [
        listening_port
    ]


def test_scan_ports_calls_progress_callback(listening_port):
    calls = []
    scan_ports(
        "127.0.0.1",
        [listening_port],
        timeout=1.0,
        workers=2,
        on_progress=lambda done, total: calls.append((done, total)),
    )
    assert calls == [(1, 1)]


def test_scan_udp_port_detects_open(udp_echo_port):
    assert scan_udp_port("127.0.0.1", udp_echo_port, timeout=1.0) == "open"


def test_scan_udp_ports_reports_open(udp_echo_port):
    assert scan_udp_ports(
        "127.0.0.1", [udp_echo_port], timeout=1.0, workers=2
    ) == [(udp_echo_port, "open")]


def test_scan_udp_port_without_response_is_ambiguous():
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()

    # UDP'de yanıtsızlık kesin bir sonuç vermez.
    assert scan_udp_port("127.0.0.1", port, timeout=0.5) in {
        "closed",
        "open|filtered",
    }
