import socket

SERVER_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

def main():
    while True:
        print("1 -> chiedere al server se un certo nome file è presente")
        print("2 -> chiedere al server il numero di frammenti di un file a partire dal suo nome file")
        print("3 -> chiedere al server l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento")
        print("4 -> chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file.")
        value=input("->")
        s.sendall(value.encode())
        if value=="1":
            risposta=s.recv(BUFFER_SIZE)
            name=input(f"{risposta.decode()}") 
            s.sendall(name.encode())
            print(s.recv(BUFFER_SIZE))
            break
        if value=="2":
            risposta=s.recv(BUFFER_SIZE)
            name=input(f"{risposta.decode()}") 
            s.sendall(name.encode())
            print(s.recv(BUFFER_SIZE))
            break
        if value=="3": 
            risposta=s.recv(BUFFER_SIZE)
            name=input(f"{risposta.decode()}") 
            s.sendall(name.encode())
            risposta=s.recv(BUFFER_SIZE)
            num=input(f"{risposta.decode()}") 
            s.sendall(num.encode())
            print(s.recv(BUFFER_SIZE))
            break
        if value=="4":
            risposta=s.recv(BUFFER_SIZE)
            name=input(f"{risposta.decode()}") 
            s.sendall(name.encode())
            print(s.recv(BUFFER_SIZE))
            break
        if value=="5":
            s.close()
        else:
            pass

        s.close()

if __name__ == "__main__":
    main()