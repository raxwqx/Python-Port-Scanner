"""portscan.output için birim testleri."""

import csv
import io
import json

from portscan.output import make_result, render_text, to_csv, to_json


def test_make_result_defaults():
    assert make_result(22) == {
        "port": 22,
        "proto": "tcp",
        "state": "open",
        "service": None,
        "banner": None,
    }


def test_render_text_includes_service_and_banner():
    results = [make_result(22, "ssh", "SSH-2.0-OpenSSH_9.6")]
    text = render_text(results)
    assert "[+] Port 22/tcp OPEN  ssh" in text
    assert "banner: SSH-2.0-OpenSSH_9.6" in text


def test_render_text_without_service_or_banner():
    assert render_text([make_result(9999)]) == "[+] Port 9999/tcp OPEN"


def test_render_text_empty():
    assert render_text([]) == ""


def test_to_json_roundtrip():
    payload = json.loads(to_json("example.com", [make_result(443, "https")]))

    assert payload["target"] == "example.com"
    assert payload["open_ports"] == 1
    assert payload["results"][0]["port"] == 443
    assert payload["results"][0]["service"] == "https"


def test_to_csv_has_header_and_rows():
    rows = list(csv.DictReader(io.StringIO(to_csv([make_result(80, "http")]))))

    assert rows == [
        {
            "port": "80",
            "proto": "tcp",
            "state": "open",
            "service": "http",
            "banner": "",
        }
    ]
