"""Günlükleme (logging) yapılandırması.

Tüm tanılama çıktısı stderr'e gider; böylece JSON/CSV sonuçları
stdout üzerinden başka araçlara aktarılabilir.
"""

import logging
import sys


class PrefixFormatter(logging.Formatter):
    """Seviyeye göre kısa önek ekleyen biçimlendirici."""

    PREFIXES = {
        logging.DEBUG: "[*]",
        logging.INFO: "[*]",
        logging.WARNING: "[!]",
        logging.ERROR: "[-]",
        logging.CRITICAL: "[-]",
    }

    def format(self, record):
        message = record.getMessage()
        if not message:
            return ""

        prefix = self.PREFIXES.get(record.levelno, "[*]")
        return f"{prefix} {message}"


def setup_logging(verbose=False):
    """`portscan` günlükleyicisini yapılandırıp döner."""
    logger = logging.getLogger("portscan")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(PrefixFormatter())
    logger.addHandler(handler)
    logger.propagate = False

    return logger
