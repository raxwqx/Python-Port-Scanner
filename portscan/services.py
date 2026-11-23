"""Port numaralarından servis adı çözümleme."""

import socket

# getservbyport her ortamda dolu olmayabilir; bilinen portlar için yedek tablo.
FALLBACK_SERVICES = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "domain",
    67: "dhcp",
    80: "http",
    110: "pop3",
    123: "ntp",
    143: "imap",
    161: "snmp",
    389: "ldap",
    443: "https",
    445: "microsoft-ds",
    465: "smtps",
    587: "submission",
    993: "imaps",
    995: "pop3s",
    1433: "ms-sql-s",
    1521: "oracle",
    2049: "nfs",
    3306: "mysql",
    3389: "ms-wbt-server",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-alt",
    8443: "https-alt",
    9200: "elasticsearch",
    27017: "mongodb",
}


def service_name(port, proto="tcp"):
    """Port için bilinen servis adını döner; bulunamazsa None."""
    try:
        return socket.getservbyport(port, proto)
    except OSError:
        return FALLBACK_SERVICES.get(port)
