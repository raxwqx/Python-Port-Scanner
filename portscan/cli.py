"""Komut satırı arayüzü."""

import argparse
import logging
import time

from .banner import grab_banner
from .core import parse_ports, resolve_target, scan_ports
from .log import setup_logging
from .output import make_result, render_text, to_csv, to_json
from .services import service_name

log = logging.getLogger("portscan")


def positive_float(value):
    """Pozitif ondalık sayı doğrulayıcı (argparse type)."""
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Geçersiz sayı: {value}") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("Değer 0'dan büyük olmalı")
    return number


def positive_int(value):
    """Pozitif tam sayı doğrulayıcı (argparse type)."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Geçersiz sayı: {value}") from None
    if number < 1:
        raise argparse.ArgumentTypeError("Değer en az 1 olmalı")
    return number


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
        type=positive_float,
        default=0.2,
        help="Bağlantı zaman aşımı, saniye (varsayılan: 0.2)",
    )
    parser.add_argument(
        "-j",
        "--workers",
        type=positive_int,
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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Ayrıntılı günlük çıktısı",
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
        log.info(f"Sonuçlar yazıldı: {output_path}")
    else:
        print(text, flush=True)


def main(argv=None):
    args = parse_args(argv)
    setup_logging(args.verbose)

    target = args.target or input("Hedef IP adresi: ").strip()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        log.error(str(exc))
        return 2

    if not ports:
        log.error("Taranacak port bulunamadı")
        return 2

    try:
        address = resolve_target(target)
    except ValueError as exc:
        log.error(str(exc))
        return 2

    if address != target:
        log.info(f"Çözümlenen adres: {address}")

    log.debug(f"Hedef: {address}, port sayısı: {len(ports)}")

    if args.format == "text":
        log.info("")
        log.info(
            f"Tarama başlıyor: {target} "
            f"({len(ports)} port, {args.workers} iş parçacığı)"
        )
        log.info("")

    started = time.perf_counter()
    try:
        open_ports = scan_ports(address, ports, args.timeout, args.workers)
    except KeyboardInterrupt:
        log.warning("Tarama kullanıcı tarafından durduruldu.")
        return 130
    elapsed = time.perf_counter() - started

    log.debug(f"Tarama {elapsed:.2f} saniyede bitti")

    results = collect_results(address, open_ports, args)

    if args.format == "json":
        write_output(to_json(target, results), args.output)
    elif args.format == "csv":
        write_output(to_csv(results), args.output)
    else:
        body = render_text(results)
        if body:
            write_output(body, args.output)
        log.info("")
        log.info(
            f"Tarama tamamlandı. "
            f"{len(open_ports)} açık port, {elapsed:.2f} saniye."
        )

    return 0
