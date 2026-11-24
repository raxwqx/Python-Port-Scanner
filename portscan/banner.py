"""Açık portlardan banner (servis imzası) okuma."""

import socket

# Bağlantı kurulur kurulmaz konuşmayan servisleri dürtmek için sırayla
# denenen yoklamalar. Her yoklama yeni bir bağlantı üzerinden yapılır.
PROBES = (
    b"\r\n",
    b"HEAD / HTTP/1.0\r\nHost: portscan\r\n\r\n",
)


def _clean(data):
    """Ham baytları tek satırlık okunur metne çevirir."""
    text = data.decode("utf-8", errors="replace").strip()
    return text or None


def _read(target, port, timeout, max_bytes, probe):
    """Bağlantı kurar, isteğe bağlı yoklamayı gönderir ve ilk veriyi döner."""
    with socket.create_connection((target, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        if probe is not None:
            sock.sendall(probe)
        return sock.recv(max_bytes)


def grab_banner(target, port, timeout=1.0, max_bytes=1024, probes=PROBES):
    """Porttan okunabilen ilk veriyi döner; okunamazsa None.

    Önce bağlantı kurulur kurulmaz gelen veri beklenir (SSH, SMTP, FTP gibi
    servisler imzalarını hemen gönderir). Servis sessiz kalırsa ``probes``
    sırayla denenir; böylece yalnızca istek gelince konuşan HTTP sunucuları
    da tanınır.
    """
    for probe in (None,) + tuple(probes):
        try:
            data = _read(target, port, timeout, max_bytes, probe)
        except OSError:
            # Zaman aşımı, bağlantı reddi veya kopma: sıradaki yoklamaya geç.
            continue

        if data:
            return _clean(data)

    return None
