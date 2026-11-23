"""Açık portlardan banner (servis imzası) okuma."""

import socket


def grab_banner(target, port, timeout=1.0, max_bytes=1024):
    """Porttan okunabilen ilk veriyi döner; okunamazsa None.

    Bazı servisler (HTTP, SMTP, FTP) bağlantı kurulur kurulmaz banner
    gönderir. Diğerleri önce istemciden veri bekler; bu durumda kısa bir
    satır sonu gönderip tekrar denenir.
    """
    try:
        with socket.create_connection((target, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            try:
                data = sock.recv(max_bytes)
            except socket.timeout:
                sock.sendall(b"\r\n")
                data = sock.recv(max_bytes)
    except OSError:
        return None

    if not data:
        return None

    text = data.decode("utf-8", errors="replace").strip()
    return text or None
