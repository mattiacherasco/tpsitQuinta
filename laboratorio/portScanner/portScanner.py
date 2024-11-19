import socket
import sqlite3
import threading

# Configurazione
SUBNET = "192.168.0."
PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 111, 143, 443, 3306, 3389]
DB_NAME = "ip_list.db"
THREAD_COUNT = 20

def init_db():
    """Crea il database e la tabella se non esiste."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hosts (
        ip_host TEXT,
        nome_host TEXT,
        port_list TEXT
    )''')
    conn.commit()
    conn.close()

def save_to_db(ip_host, nome_host, port_list):
    """Salva i dati nel database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO hosts (ip_host, nome_host, port_list) VALUES (?, ?, ?)", 
              (ip_host, nome_host, ', '.join(map(str, port_list))))
    conn.commit()
    conn.close()

def scan_host(ip):
    """Scansiona un host per porte aperte."""
    open_ports = []
    try:
        nome_host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        nome_host = None

    for port in PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    
    if open_ports:
        save_to_db(ip, nome_host, open_ports)
        print(f"[+] {ip} ({nome_host}) -> Porte aperte: {open_ports}")
    else:
        print(f"[-] {ip} -> Nessuna porta aperta")

def scan_subnet(start, end):
    """Scansiona un intervallo di indirizzi IP nella subnet."""
    for i in range(start, end):
        ip = f"{SUBNET}{i}"
        scan_host(ip)

def consult_db():
    """Interroga il database per ottenere gli IP con nome host e porte aperte."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ip_host, nome_host, port_list FROM hosts WHERE nome_host IS NOT NULL")
    results = c.fetchall()
    conn.close()
    return results

def main():
    init_db()
    
    print("[*] Inizio scansione...")
    threads = []
    step = 32 // THREAD_COUNT  # Divide il range degli IP tra i thread
    
    for i in range(THREAD_COUNT):
        start = i * step
        end = start + step if i < THREAD_COUNT - 1 else 32
        t = threading.Thread(target=scan_subnet, args=(start, end))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print("[*] Scansione completata!")
    
    print("[*] Consultazione database:")
    results = consult_db()
    for ip_host, nome_host, port_list in results:
        print(f"IP: {ip_host}, Host: {nome_host}, Porte Aperte: {port_list}")

if __name__ == "__main__":
    main()
