# 🐍 Python Port Scanner

Basit ve hafif bir Python TCP port tarayıcısıdır.

Bu proje, Python `socket` modülünü ve temel ağ bağlantılarını öğrenmek amacıyla geliştirilmiştir.

## ✨ Özellikler

- 🔎 TCP portlarını tarar
- 🟢 Açık portları gösterir
- 🐍 Python `socket` modülünü kullanır
- ⚡ 1-1024 arasındaki portları kontrol eder
- 🧪 Eğitim ve kontrollü lab ortamları için tasarlanmıştır

## 📋 Gereksinimler

- Python 3

Python sürümünü kontrol etmek için:

```bash
python3 --version
```

## 🚀 Kullanım

Projeyi indirdikten sonra:

```bash
python3 scanner.py
```

Program hedef IP adresini soracaktır:

```text
Hedef IP adresi: 127.0.0.1
```

Ardından 1-1024 arasındaki TCP portları kontrol edilir.

## 📌 Örnek Çıktı

```text
[*] Tarama başlıyor: 127.0.0.1

[+] Port 22 OPEN
[+] Port 80 OPEN
[+] Port 443 OPEN

[*] Tarama tamamlandı.
```

## ⚙️ Nasıl Çalışır?

Program Python'un `socket` modülünü kullanarak hedef sistemdeki TCP portlarına bağlantı kurmayı dener.

Bağlantı başarılı olursa port:

```text
OPEN
```

olarak gösterilir.

Bağlantı kurulamazsa port açık olarak gösterilmez.

## ⚠️ Yasal Uyarı

Bu araç yalnızca kendi sistemlerinizde, CTF ortamlarında veya açıkça izin verilen kontrollü sistemlerde kullanılmalıdır.

İzinsiz sistemleri taramak yasal ve etik sorunlara neden olabilir.

## 📚 Öğrenme Amaçlı

Bu proje aşağıdaki konuları öğrenmek için hazırlanmıştır:

- Python Socket Programming
- TCP/IP
- Portlar
- Ağ bağlantıları
- Temel Network Security

## 📄 License

MIT License
