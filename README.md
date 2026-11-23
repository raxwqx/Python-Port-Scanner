# 🐍 Python Port Scanner

[![CI](https://github.com/raxwqx/Python-Port-Scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/raxwqx/Python-Port-Scanner/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Lisans](https://img.shields.io/badge/lisans-MIT-green)](LICENSE)

Python standart kütüphanesi ile yazılmış, bağımlılığı olmayan bir TCP port
tarayıcısı. Eğitim, CTF ve kontrollü laboratuvar ortamları için tasarlandı.

## ✨ Özellikler

- ⚡ **Paralel tarama** — `ThreadPoolExecutor` ile yapılandırılabilir eşzamanlılık
- 🎯 **Esnek port seçimi** — `1-1024`, `22,80,443`, `1-100,8080` veya hazır listeler
- 🏷️ **Servis adı çözümleme** — `22/tcp OPEN ssh`
- 📡 **Banner okuma** — açık portlardan servis imzası (`SSH-2.0-OpenSSH_9.6`)
- 📄 **Çıktı biçimleri** — insan okunur metin, JSON, CSV; dosyaya yazma
- 🎚️ **Günlük seviyeleri** — `-v` ayrıntılı, `-q` sessiz; tanılama stderr'de
- 📊 **İlerleme göstergesi** — uzun taramalarda canlı yüzde
- 🧪 **42 birim testi** — gerçek soketler üzerinden, ağ erişimi gerektirmez
- 🐳 **Docker imajı** — root olmayan kullanıcı ile çalışır

## 📋 Gereksinimler

- Python **3.9** veya üzeri
- Harici paket gerekmez (testler için `pytest`)

```bash
python3 --version
```

## 🚀 Kurulum

Depoyu klonlayıp doğrudan çalıştırabilirsiniz:

```bash
git clone https://github.com/raxwqx/Python-Port-Scanner.git
cd Python-Port-Scanner
python3 scanner.py --help
```

`portscan` komutu olarak kurmak için:

```bash
pip install -e .
portscan --help
```

Docker ile:

```bash
docker build -t portscan .
docker run --rm portscan --version
```

## ⚡ Hızlı Başlangıç

```bash
# 1-1024 arası portları tara
python3 -m portscan 127.0.0.1

# Yalnızca belirli portlar
python3 -m portscan -p 22,80,443 127.0.0.1

# Hazır liste ile hızlı tarama
python3 -m portscan --preset top100 192.168.1.10

# JSON çıktısını dosyaya yaz
python3 -m portscan -p 1-1024 -f json -o sonuc.json 127.0.0.1
```

## 📖 Kullanım

```text
portscan [target] [seçenekler]
```

| Seçenek | Açıklama | Varsayılan |
| --- | --- | --- |
| `target` | Hedef IP adresi veya alan adı | etkileşimli sorulur |
| `-p, --ports` | Port tanımı: `1-1024`, `22,80,443`, `1-100,8080` | `1-1024` |
| `--preset` | Hazır port listesi (`--list-presets` ile listele) | — |
| `--list-presets` | Hazır listeleri ve port sayılarını göster | — |
| `-t, --timeout` | Bağlantı zaman aşımı (saniye) | `0.2` |
| `-j, --workers` | Eşzamanlı tarama sayısı | `100` |
| `--banner` | Açık portlardan banner okumayı dene | kapalı |
| `--no-service` | Servis adı çözümlemesini kapat | kapalı |
| `-f, --format` | Çıktı biçimi: `text`, `json`, `csv` | `text` |
| `-o, --output` | Sonuçları dosyaya yaz (`-` = stdout) | — |
| `-v, --verbose` | Ayrıntılı günlük çıktısı | — |
| `-q, --quiet` | Yalnızca sonuçları göster | — |
| `-V, --version` | Sürümü göster | — |

### Hazır port listeleri

| Liste | İçerik |
| --- | --- |
| `top20` | En yaygın 20 port |
| `top100` | Nmap'in ilk 100 portu |
| `web` | 80, 443, 3000, 5000, 8000, 8080, 8081, 8443, 8888 |
| `db` | 1433, 1521, 3306, 5432, 6379, 9042, 11211, 27017 |
| `mail` | 25, 110, 143, 465, 587, 993, 995 |
| `remote` | 22, 23, 3389, 5900, 5985, 5986 |

```bash
python3 -m portscan --list-presets
```

## 📌 Örnek Çıktı

```text
[*] Tarama başlıyor: 127.0.0.1 (1024 port, 100 iş parçacığı)

[+] Port 22/tcp OPEN  ssh
[+] Port 80/tcp OPEN  http
[+] Port 443/tcp OPEN  https

[*] Tarama tamamlandı. 3 açık port, 0.84 saniye.
```

Banner ile:

```bash
python3 -m portscan -p 22,80 --banner 127.0.0.1
```

```text
[+] Port 22/tcp OPEN  ssh
    banner: SSH-2.0-OpenSSH_9.6
```

JSON çıktısı (`-f json`):

```json
{
  "target": "127.0.0.1",
  "open_ports": 1,
  "results": [
    {
      "port": 22,
      "proto": "tcp",
      "state": "open",
      "service": "ssh",
      "banner": null
    }
  ]
}
```

Tanılama çıktısı stderr'e gittiği için JSON doğrudan boru hattında kullanılabilir:

```bash
python3 -m portscan -f json 127.0.0.1 | jq '.results[].port'
```

## ⚙️ Nasıl Çalışır?

1. Hedef alan adı **bir kez** IPv4 adresine çözülür.
2. Port listesi ayrıştırılır ve tekilleştirilir.
3. Her port için `socket.connect_ex()` ile TCP bağlantısı denenir; bağlantı
   kurulabiliyorsa port açık kabul edilir.
4. Sonuçlar istenen biçimde yazdırılır veya dosyaya kaydedilir.

`connect_ex` üç yönlü el sıkışmayı tamamladığı için yalnızca gerçekten
dinleyen servisleri "açık" olarak raporlar. Filtrelenen portlar zaman
aşımına uğrar ve sonuçlara dahil edilmez.

## 🧪 Geliştirme

```bash
pip install -e ".[dev]"
python3 -m pytest
```

Testler gerçek soketler kullanır ama yalnızca `127.0.0.1` üzerinde çalışır.
CI, Python 3.9–3.13 matrisinde testleri, CLI duman testini ve Docker imaj
derlemesini çalıştırır.

Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

## 📁 Proje Yapısı

```text
.
├── portscan/
│   ├── cli.py        # argümanlar ve akış
│   ├── core.py       # hedef çözümleme, port ayrıştırma, tarama
│   ├── services.py   # servis adı çözümleme
│   ├── banner.py     # banner okuma
│   ├── output.py     # text / JSON / CSV biçimlendirme
│   ├── presets.py    # hazır port listeleri
│   └── log.py        # günlükleme yapılandırması
├── tests/
├── scanner.py        # geriye dönük uyumlu giriş noktası
├── Dockerfile
└── pyproject.toml
```

## ⚠️ Yasal Uyarı

Bu araç yalnızca **kendi sistemlerinizde**, CTF ortamlarında veya açıkça
izin verilen kontrollü sistemlerde kullanılmalıdır.

İzinsiz sistemleri taramak birçok ülkede yasal ve etik sorunlara yol açar.
Sorumluluk kullanıcıya aittir.

## 📚 Öğrenme Amaçlı

Bu proje şu konuları öğrenmek için hazırlanmıştır:

- Python socket programlama ve TCP/IP
- Portlar ve servisler
- Eşzamanlı programlama (`ThreadPoolExecutor`)
- Test yazımı (`pytest`) ve CI
- Temel ağ güvenliği

## 📄 Lisans

[MIT](LICENSE)
