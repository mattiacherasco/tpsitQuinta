import socket
import threading
from pynput import keyboard
import time

SERVER_ADDRESS = ("192.168.1.121", 9600)
HEARTBEAT_ADDRESS = ("192.168.1.121",9601)
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

#facciamo thread per inviare sempre messaggi a alpha per gestire heartbeat
def send_heartbeat():
    heart_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heart_socket.connect(HEARTBEAT_ADDRESS)
    while True:
        try:
            heart_socket.sendall("ciao").encode()
            time.sleep(1)  #mando ciao ogni secondo
        except Exception as e:
            print(f"Errore durante l'invio dell'heartbeat: {e}")
            break
    heart_socket.close()

def on_press(key):
    try:
        if key.char in ["w", "s", "a", "d"]:
            s.sendall(key.char.encode())
    except AttributeError:
        pass  

def on_release(key):
    try:
        if key.char in ["w", "s", "a", "d"]:
            s.sendall(key.char.upper().encode())
    except AttributeError:
        pass  

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.start()

    start_listener()

    # mantengo main thread attivo e continua ad "ascoltare" i tasti
    while True:
        pass

    s.close()

if __name__ == "__main__":
    main()