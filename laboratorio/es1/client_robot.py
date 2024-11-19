import socket
SERVER_ADDRESS=("192.168.1.121",9000)
BUFFER_SIZE=4096

def main():
    diz ={"0":"quit", "1":"backward", "2":"forward", "3":"right", "4":"left"}
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    while True:
            print("choose your move:")
            print(diz)

            choice = input("choose the number-> ")
            if choice == '0':
                break
            elif choice in diz:
                time = int(input("choose the time in seconds -> "))
                s.sendall(f"{diz[choice]}|{time}".encode())
                data = s.recv(1024)
                print(f"{data.decode().replace(f"|",": ")}")
            else:
                print(f"{choice} not in diz")

if __name__=="__main__":
    main()