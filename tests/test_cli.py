"""portscan.cli için uçtan uca testler."""

import json

import pytest

from portscan import __version__
from portscan.cli import main, parse_args


def test_parse_args_defaults():
    args = parse_args(["127.0.0.1"])

    assert args.target == "127.0.0.1"
    assert args.ports is None
    assert args.preset is None
    assert args.timeout == 0.2
    assert args.workers == 100
    assert args.format == "text"


def test_parse_args_preset_and_ports_conflict():
    with pytest.raises(SystemExit):
        parse_args(["--preset", "web", "-p", "80", "127.0.0.1"])


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as excinfo:
        parse_args(["--version"])

    assert excinfo.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_list_presets(capsys):
    assert main(["--list-presets"]) == 0
    assert "top100" in capsys.readouterr().out


def test_main_invalid_port_returns_2(capsys):
    assert main(["-p", "0", "127.0.0.1"]) == 2
    assert "Geçersiz port" in capsys.readouterr().err


def test_main_invalid_host_returns_2(capsys):
    assert main(["-p", "80", "bu-hedef-gecersiz.invalid"]) == 2
    assert "çözümlenemedi" in capsys.readouterr().err.lower()


def test_main_scan_open_port(listening_port, capsys):
    assert main(["-p", str(listening_port), "127.0.0.1", "-q"]) == 0
    assert f"Port {listening_port}/tcp OPEN" in capsys.readouterr().out


def test_main_json_output(listening_port, capsys):
    assert main(["-p", str(listening_port), "127.0.0.1", "-f", "json", "-q"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["open_ports"] == 1
    assert payload["results"][0]["port"] == listening_port


def test_main_writes_output_file(listening_port, tmp_path, capsys):
    target = tmp_path / "sonuc.csv"

    assert main(
        ["-p", str(listening_port), "127.0.0.1", "-f", "csv", "-o", str(target)]
    ) == 0

    assert "port,proto,state,service,banner" in target.read_text(encoding="utf-8")
    assert str(target) in capsys.readouterr().err
