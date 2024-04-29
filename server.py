import socket
import threading

BYTESIZE = 900000
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DSICONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}  connected")

    connected = True
    while connected:
        msg_length = conn.recv(BYTESIZE).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}] {msg}")

        if msg == DISCONNECT_MESSAGE:
            connected = False;

    

def start():
    server.listen()
    print(f"[LISTENING] listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args =(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
    

print("[STARTING] serer is starting....")
start()