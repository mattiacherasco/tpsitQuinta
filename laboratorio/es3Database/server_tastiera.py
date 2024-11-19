import socket
import threading
import RPi.GPIO as GPIO
import sqlite3
import time
l=r=0
MY_ADDRESS = ("192.168.1.124", 9600)
HEARTBEAT_ADDRESS = ("192.168.1.124", 9601)  # Porta separata per l'heartbeat ma stesso indirizz
BUFFER_SIZE = 4096
SEPARATOR=","

class AlphaBot(object):
    def __init__(self, in1=12, in2=13, ena=6, in3=20, in4=21, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(50)  
        self.PWMB.start(50)

    def forward(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def backward(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def right(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def calcolateMove(self, tupla):
        # Stampa i dati
        string=tupla[0]
        comandi=[{"azione":comando[0], "valore":int(comando[1:])} for comando in string.split(SEPARATOR)]
        for comando in comandi:
            x=comando["azione"]
            if x == "f":
                print("avanti")
                l=r=100
            elif x == "b":
                print("indietro")
                l=r=-100
            elif x == "l":
                print("sinistra")
                l=100
                r=-100
            elif x == "r":
                print("destra")
                l=-100
                r=100
            self.setMotor(l,r)
            time.sleep(comando["valore"])
            self.stop()
    
    def readDb(self, letter):
        conn = sqlite3.connect('alphabot.db')
        c = conn.cursor()
        # Recupera tutti i dati dalla tabella 'commands'
        c.execute(f'SELECT command FROM commands WHERE commands.letter="{letter}"')
        tuplaDb = c.fetchone()
        if tuplaDb is not None:
            self.calcolateMove(tuplaDb)
        else:    
            print("tupla null")
        conn.close()
    
    def setMotor(self, left, right):
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def heartbeat_receive(heart_socket, alphaBot):
    heart_socket.settimeout(6.5)  #timeout di 6.5 secondi l'heartbeat
    try:
        while True:
            try:
                data = heart_socket.recv(BUFFER_SIZE)
                if not data:
                    print("Connessione heartbeat chiusa.")
                    break
                print("Heartbeat ricevuto: up")
            except socket.timeout:
                print("Heartbeat timeout! FERMA TUTTO")
                alphaBot.stop()
                break
            except Exception as e:
                print(f"Errore heartbeat: {e}")
                break
    finally:
        heart_socket.close()

def main():
    alphaBot = AlphaBot()
    alphaBot.stop()

    #controllo del movimento
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen(1)

    # controllo l'heartbeat
    heart_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heart_socket.bind(HEARTBEAT_ADDRESS)
    heart_socket.listen(1)

    try:
        connection, client_address = s.accept()
        print(f"Il client {client_address} si è connesso")
        
        heartbeat_conn, _ = heart_socket.accept()
        print("Connessione heartbeat ok")

        # avvio thread separato per l'heartbeat
        heartbeat_thread = threading.Thread(target=heartbeat_receive, args=(heartbeat_conn, alphaBot))
        heartbeat_thread.start()

        #gestione dei comandi di movimento con main thread
        while True:
            try:
                message = connection.recv(BUFFER_SIZE)
                if not message:
                    print("Connessione chiusa dal client.")
                    break

                direz_decode = message.decode()               
                if direz_decode == "a":
                    print("avanti")
                    l=r=100
                elif direz_decode == "d":
                    print("indietro")
                    l=r=-100
                elif direz_decode == "w":
                    print("sinistra")
                    l=-100
                    r=100
                elif direz_decode == "s":
                    print("destra")
                    l=100
                    r=-100
                elif direz_decode.isupper():
                    l=r=0
                    alphaBot.stop()
                else:
                    alphaBot.readDb(direz_decode)
                alphaBot.setMotor(l,r)
            except Exception as e:
                print(f"Errore nella ricezione dei comandi: {e}")

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        #chiudo tutto
        s.close()
        heart_socket.close()


if __name__ == "__main__":
    main()