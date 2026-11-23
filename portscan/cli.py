"""Komut satırı arayüzü."""

import argparse
import sys
import time

from .banner import grab_banner
from .core import parse_ports, scan_ports
from .services import service_name


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
    parser.add_argument(
        "--banner",
        action="store_true",
        help="Açık portlardan banner (servis imzası) okumayı dene",
    )
    parser.add_argument(
        "--no-service",
        action="store_true",
        help="Portlar için servis adı çözümlemesini kapat",
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
        name = None if args.no_service else service_name(port)
        suffix = f"  {name}" if name else ""
        print(f"[+] Port {port}/tcp OPEN{suffix}")

        if args.banner:
            banner = grab_banner(target, port, timeout=max(args.timeout, 1.0))
            if banner:
                first_line = banner.splitlines()[0][:120]
                print(f"    banner: {first_line}")

    print(
        f"\n[*] Tarama tamamlandı. "
        f"{len(open_ports)} açık port, {elapsed:.2f} saniye."
    )
    return 0
