import socket
import threading
import sqlite3

MY_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

def task12(nome, query):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    c.execute(query, (nome,))
    tuplaDb = c.fetchone()
    conn.close()
    return tuplaDb if tuplaDb is not None else None
    
def task3(nome, num, query):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    c.execute(query, (nome, num))
    tuplaDb = c.fetchone()
    conn.close()
    return tuplaDb if tuplaDb is not None else None

def task4(nome, query):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    c.execute(query, (nome,))
    tuplaDb = c.fetchone()
    conn.close()
    return tuplaDb if tuplaDb is not None else None    

def handle_client(connection, client_address):
    print(f"Il client {client_address} si è connesso")
    while True:
        message = connection.recv(BUFFER_SIZE)
        if not message:
            print(f"Connessione chiusa dal client {client_address}.")
            break
        
        messages = message.decode()
        print(f"Messaggio ricevuto da {client_address}: {messages}")
        
        if messages == "1":
            connection.sendall("inserire il nome da ricecare -> ".encode())
            nome = connection.recv(BUFFER_SIZE).decode()
            if task12(nome, 'SELECT nome FROM files WHERE nome = ?'):
                connection.sendall("nome presente".encode())
            else:
                connection.sendall("nome non presente".encode())
                
        elif messages == "2":
            connection.sendall("inserire il nome di cui si vuole sapere il totale di frammenti -> ".encode())
            nome = connection.recv(BUFFER_SIZE).decode()
            result = task12(nome, 'SELECT tot_frammenti FROM files WHERE nome = ?')
            connection.sendall(f"{result}".encode())
            
        elif messages == "3":
            connection.sendall("inserire il nome di cui si vuole sapere il totale di frammenti -> ".encode())
            nome = connection.recv(BUFFER_SIZE).decode()
            connection.sendall("inserire il numero del frammento di cui si vuole sapere l'host -> ".encode())
            num = connection.recv(BUFFER_SIZE).decode()
            result = task3(nome, num, "SELECT host FROM files, frammenti WHERE nome = ? AND files.id_file == frammenti.id_file AND frammenti.n_frammento=?")
            connection.sendall(f"{result}".encode())
            
        elif messages == "4":
            connection.sendall("inserire il nome di cui si vuole sapere il totale di frammenti -> ".encode())
            nome = connection.recv(BUFFER_SIZE).decode()
            result = task4(nome, 'SELECT host FROM files, frammenti WHERE nome = ? AND files.id_file == frammenti.id_file')
            connection.sendall(f"{result}".encode())
            
        elif messages == "5":
            print(f"Il client {client_address} ha chiuso la connessione.")
            break
    
    connection.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    print("Server in ascolto...")
    
    while True:
        connection, client_address = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
