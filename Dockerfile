# syntax=docker/dockerfile:1

FROM python:3.12-slim

LABEL org.opencontainers.image.title="Python Port Scanner" \
      org.opencontainers.image.description="Basit TCP port tarayıcısı (eğitim amaçlı)" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/raxwqx/Python-Port-Scanner"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Önce yalnızca bağımlılık tanımını kopyalayıp katman önbelleğinden yararlan.
COPY pyproject.toml README.md ./
COPY portscan ./portscan
COPY scanner.py ./

RUN pip install --no-cache-dir .

# Root olmayan kullanıcı ile çalıştır.
RUN useradd --create-home --uid 1000 scanner
USER scanner

ENTRYPOINT ["portscan"]
CMD ["--help"]
