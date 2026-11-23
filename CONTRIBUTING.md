# Katkı Rehberi

Katkıda bulunmak istediğiniz için teşekkürler! 🐍

## Geliştirme Ortamı

```bash
git clone https://github.com/raxwqx/Python-Port-Scanner.git
cd Python-Port-Scanner
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Testler

Tüm testler standart kütüphane ile yazılmıştır; harici ağ erişimi
gerektirmezler. Değişiklik göndermeden önce mutlaka çalıştırın:

```bash
python3 -m pytest
```

Tek bir testi çalıştırmak için:

```bash
python3 -m pytest tests/test_cli.py::test_main_json_output -v
```

## Kod Tarzı

- PEP 8'e uyun; satır uzunluğu 88 karakteri geçmesin.
- Python 3.9+ ile uyumlu kalın (CI bu sürümü de test eder).
- Tanılama mesajları için `print` yerine `portscan/log.py` üzerinden `logging` kullanın.
- Sonuç üretimi (stdout) ile tanılama (stderr) çıktısını karıştırmayın.
- Yeni bir özellik ekliyorsanız testini de ekleyin.

## Commit Mesajları

Kısa, emir kipinde ve ne yapıldığını anlatan mesajlar yazın:

```text
Add UDP scanning mode
Fix timeout handling for unreachable hosts
```

## Dal ve Pull Request Akışı

1. `main` dalından yeni bir dal açın: `feat/kisa-ad`, `fix/kisa-ad`, `docs/kisa-ad`.
2. Değişikliğinizi küçük ve odaklı tutun.
3. Testlerin geçtiğinden emin olun.
4. PR açıklamasında **ne değişti**, **neden** ve **nasıl test edildi** bölümlerini doldurun.

## Yasal Sınır

Bu araç yalnızca eğitim ve izin verilen sistemlerde kullanılmak üzere
geliştirilmiştir. Testlerinizi `127.0.0.1`, kendi laboratuvarınız veya
açıkça izin verilen hedeflerde yapın. İzinsiz tarama içeren katkılar
kabul edilmez.
