"""Basit TCP port tarayıcısı.

Eğitim ve kontrollü lab ortamları için yazılmıştır. Yalnızca kendi
sistemlerinizde veya açıkça izin verilen hedeflerde kullanın.
"""

import argparse
import socket
import sys


def parse_args(argv=None):
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        prog="scanner.py",
        description="Basit TCP port tarayıcısı (eğitim amaçlı).",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Hedef IP adresi veya alan adı (verilmezse sorulur)",
    )
    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help="Port aralığı: '1-1024', '22,80,443' veya '1-100,8080' (varsayılan: 1-1024)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.2,
        help="Bağlantı zaman aşımı, saniye (varsayılan: 0.2)",
    )
    return parser.parse_args(argv)


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


def main(argv=None):
    args = parse_args(argv)

    target = args.target or input("Hedef IP adresi: ").strip()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print(f"[-] {exc}", file=sys.stderr)
        return 2

    print(f"\n[*] Tarama başlıyor: {target}\n")

    for port in ports:
        if scan_port(target, port, args.timeout):
            print(f"[+] Port {port} OPEN")

    print("\n[*] Tarama tamamlandı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
