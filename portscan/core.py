"""Tarama çekirdeği: hedef çözümleme, port ayrıştırma ve TCP denemeleri."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def resolve_target(target):
    """Hedefi IPv4 adresine çözer; çözülemezse ValueError fırlatır."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror as exc:
        detail = exc.strerror or str(exc)
        raise ValueError(f"Hedef çözümlenemedi: {target} ({detail})") from exc


def parse_ports(spec):
    """'1-1024' veya '22,80,443' biçimindeki port tanımını listeye çevirir."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            try:
                start, end = int(start_text), int(end_text)
            except ValueError:
                raise ValueError(f"Geçersiz port tanımı: {part}") from None
            if start > end:
                raise ValueError(f"Geçersiz port aralığı: {part}")
            ports.update(range(start, end + 1))
        else:
            try:
                ports.add(int(part))
            except ValueError:
                raise ValueError(f"Geçersiz port tanımı: {part}") from None

    for port in ports:
        if not 1 <= port <= 65535:
            raise ValueError(f"Geçersiz port numarası: {port}")

    return sorted(ports)


def scan_port(target, port, timeout=0.2):
    """Tek bir TCP portuna bağlanmayı dener; açıksa True döner.

    Soket hataları (izin, ağ erişimi, zaman aşımı) "kapalı" olarak
    değerlendirilir; tarama tek bir port yüzünden durmaz.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((target, port)) == 0
    except OSError:
        return False


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
