import socket
import threading
import os

BYTESIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # Corrected spelling

CURRENTDIR = os.getcwd()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}  connected")
    pather = ""

    connected = True
    while connected:
        msg_length = conn.recv(BYTESIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            if msg == "application/pdf":
                conn.send("PDF file type received".encode(FORMAT))
                name = socket.gethostbyaddr(addr[0])[0]
                pather = CURRENTDIR + "/received" +f"/{name}"
                foldercreator(name)

                # Receive filename
                filename_length = int(conn.recv(BYTESIZE).decode(FORMAT))
                filename = conn.recv(filename_length).decode(FORMAT)
                conn.send("Filename received".encode(FORMAT))

                fullpath = os.path.join(pather, filename)

                # Receive file content
                with open(fullpath, 'wb') as file:
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        file.write(chunk)

                print(f"[{addr}] File received: {filename}")
                conn.send("File received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args =(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

def foldercreator(devicename):
    path = CURRENTDIR + "/received"
    if os.path.exists(path):
        path2 = path + f"/{devicename}"

        if not os.path.exists(path2):
            os.makedirs(path2)
        else:
            pass

    else:
        dir = path + f"/{devicename}"
        os.makedirs(dir)

print("[STARTING] server is starting....") 
start()
