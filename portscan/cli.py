"""Komut satırı arayüzü."""

import argparse
import sys
import time

from .banner import grab_banner
from .core import parse_ports, scan_ports
from .output import make_result, render_text, to_csv, to_json
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
    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Çıktı biçimi (varsayılan: text)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="DOSYA",
        help="Sonuçları dosyaya yaz ('-' standart çıktı)",
    )
    return parser


def parse_args(argv=None):
    """Komut satırı argümanlarını ayrıştırır."""
    return build_parser().parse_args(argv)


def collect_results(target, open_ports, args):
    """Açık portları servis/banner bilgisiyle sonuç kayıtlarına dönüştürür."""
    results = []
    for port in open_ports:
        service = None if args.no_service else service_name(port)

        banner = None
        if args.banner:
            raw = grab_banner(target, port, timeout=max(args.timeout, 1.0))
            if raw:
                banner = raw.splitlines()[0][:120]

        results.append(make_result(port, service, banner))
    return results


def write_output(text, output_path):
    """Üretilen çıktıyı dosyaya veya standart çıktıya yazar."""
    if output_path and output_path != "-":
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(text.rstrip("\n") + "\n")
        print(f"[*] Sonuçlar yazıldı: {output_path}", file=sys.stderr)
    else:
        print(text)


def main(argv=None):
    args = parse_args(argv)

    target = args.target or input("Hedef IP adresi: ").strip()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print(f"[-] {exc}", file=sys.stderr)
        return 2

    if args.format == "text":
        print(
            f"\n[*] Tarama başlıyor: {target} "
            f"({len(ports)} port, {args.workers} iş parçacığı)\n"
        )

    started = time.perf_counter()
    open_ports = scan_ports(target, ports, args.timeout, args.workers)
    elapsed = time.perf_counter() - started

    results = collect_results(target, open_ports, args)

    if args.format == "json":
        write_output(to_json(target, results), args.output)
    elif args.format == "csv":
        write_output(to_csv(results), args.output)
    else:
        body = render_text(results)
        if body:
            write_output(body, args.output)
        print(
            f"\n[*] Tarama tamamlandı. "
            f"{len(open_ports)} açık port, {elapsed:.2f} saniye."
        )

    return 0
