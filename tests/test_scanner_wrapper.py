"""scanner.py uyumluluk sarmalayıcısı için testler."""

import subprocess
import sys
from pathlib import Path

import scanner
from portscan.cli import main

ROOT = Path(__file__).resolve().parent.parent


def test_wrapper_exposes_the_same_main():
    """Sarmalayıcı, paketin gerçek giriş noktasını dışa açmalı."""
    assert scanner.main is main


def test_script_reports_version():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scanner.py"), "--version"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=ROOT,
    )

    assert result.returncode == 0
    assert "portscan" in result.stdout


def test_script_lists_presets():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scanner.py"), "--list-presets"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=ROOT,
    )

    assert result.returncode == 0
    assert "top100" in result.stdout
