"""Tarama sonuçlarını metin, JSON ve CSV biçimlerinde üretme."""

import csv
import io
import json

FIELDS = ["port", "proto", "state", "service", "banner"]


def make_result(port, service=None, banner=None, proto="tcp", state="open"):
    """Tek bir açık port için sonuç kaydı üretir."""
    return {
        "port": port,
        "proto": proto,
        "state": state,
        "service": service,
        "banner": banner,
    }


def render_text(results):
    """Sonuçları insan tarafından okunur biçimde döner."""
    lines = []
    for result in results:
        suffix = f"  {result['service']}" if result.get("service") else ""
        state = str(result.get("state", "open")).upper()
        lines.append(f"[+] Port {result['port']}/{result['proto']} {state}{suffix}")
        if result.get("banner"):
            lines.append(f"    banner: {result['banner']}")
    return "\n".join(lines)


def to_json(target, results):
    """Sonuçları JSON metnine çevirir."""
    payload = {"target": target, "open_ports": len(results), "results": results}
    return json.dumps(payload, indent=2, ensure_ascii=False)


def to_csv(results):
    """Sonuçları CSV metnine çevirir."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(results)
    return buffer.getvalue()
