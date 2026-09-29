import socket

target = input("Hedef IP adresi: ")

print(f"\n[*] Tarama başlıyor: {target}\n")

for port in range(1, 1025):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"[+] Port {port} OPEN")

    sock.close()

print("\n[*] Tarama tamamlandı.")
