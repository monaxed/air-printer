import hashlib
import socket
import threading
import os
import sys
import time

BYTESIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DSICONNECT"

CURRENTDIR = os.getcwd()
pather = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}  connected")
    connected = True
    while connected:
        msg = conn.recv(1024).decode()
        print(msg)
        # conn.send("File type receive".encode(FORMAT))

        if msg == DISCONNECT_MESSAGE or msg == "":
            connected = False
        
        if msg == "application/pdf":
            name = conn.recv(1024).decode()
            print(name)
            # conn.send("name received".encode(FORMAT))
            devicename = socket.gethostbyaddr(addr[0])[0]
            foldercreator(devicename)
            
            content = b""
            done = False
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                content += data
                if content.endswith(b"<END>"):
                    break

            # while not done:
            #     data = conn.recv(1024)
            #     if content[-5:] == b"<END>" or data == "":
            #         done = True
            #         print("stopped")
            #     else:
            #         content += data
            #         print("mistake")

                
            conn.send("File content received".encode(FORMAT))
            path = pather + f"/{name}"
            writer(path, content)
            clear_buffer(conn, len(content))
            print("done")
            
            # print(f"[{addr}] {msg}")
            # conn.send("Msg received".encode(FORMAT))
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
    global pather
    if os.path.exists(path):
        path2 = path + f"/{devicename}"

        if not os.path.exists(path2):
            os.makedirs(path2)
            pather = path2
        else:
            pass

    else:
        dir = path + f"/{devicename}"
        os.makedirs(dir)
        pather = dir

def writer(path, content):
    file = open(path, "wb")
    file.write(content)
    file.close()
    print("here")

def clear_buffer(conn, size):
    # Set a timeout to prevent blocking indefinitely
    conn.settimeout(0.1)  # Adjust the timeout as needed
    
    # Read data until the buffer is empty
    while True:
        try:
            data = conn.recv(size)  # Adjust buffer size as needed
            if not data:
                break  # No more data in the buffer
        except socket.timeout:
            break  # Timeout reached, no more data in the buffer
        except socket.error as e:
            # Handle socket errors if necessary
            print("Socket error:", e)
            break

def calculate_checksum(data):
    """Calculate the MD5 checksum of byte data."""
    hasher = hashlib.md5()
    hasher.update(data)
    return hasher.hexdigest()

print("[STARTING] serer is starting....") 
start()