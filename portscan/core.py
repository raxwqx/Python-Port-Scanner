"""Tarama çekirdeği: port ayrıştırma ve TCP bağlantı denemeleri."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_ports(spec):
    """'1-1024' veya '22,80,443' biçimindeki port tanımını listeye çevirir."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
            if start > end:
                raise ValueError(f"Geçersiz port aralığı: {part}")
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))

    for port in ports:
        if not 1 <= port <= 65535:
            raise ValueError(f"Geçersiz port numarası: {port}")

    return sorted(ports)


def scan_port(target, port, timeout=0.2):
    """Tek bir TCP portuna bağlanmayı dener; açıksa True döner."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((target, port)) == 0


def scan_ports(target, ports, timeout=0.2, workers=100):
    """Portları paralel olarak tarar ve açık olanların sıralı listesini döner."""
    open_ports = []

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(scan_port, target, port, timeout): port for port in ports
        }
        for future in as_completed(futures):
            if future.result():
                open_ports.append(futures[future])

    return sorted(open_ports)
