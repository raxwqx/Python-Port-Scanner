"""Komut satırı arayüzü."""

import argparse
import sys
import time

from .core import parse_ports, scan_ports


def build_parser():
    """argparse ayrıştırıcısını oluşturur."""
    parser = argparse.ArgumentParser(
        prog="portscan",
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
    parser.add_argument(
        "-j",
        "--workers",
        type=int,
        default=100,
        help="Eşzamanlı tarama sayısı (varsayılan: 100)",
    )
    return parser


def parse_args(argv=None):
    """Komut satırı argümanlarını ayrıştırır."""
    return build_parser().parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    target = args.target or input("Hedef IP adresi: ").strip()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print(f"[-] {exc}", file=sys.stderr)
        return 2

    print(
        f"\n[*] Tarama başlıyor: {target} "
        f"({len(ports)} port, {args.workers} iş parçacığı)\n"
    )

    started = time.perf_counter()
    open_ports = scan_ports(target, ports, args.timeout, args.workers)
    elapsed = time.perf_counter() - started

    for port in open_ports:
        print(f"[+] Port {port} OPEN")

    print(
        f"\n[*] Tarama tamamlandı. "
        f"{len(open_ports)} açık port, {elapsed:.2f} saniye."
    )
    return 0
