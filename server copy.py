import hashlib
import socket
import threading
import os
import sys
import time

BYTESIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DSICONNECT"

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
                connected = False;
            
            if msg == "application/pdf":
                conn.send("PDF file type received".encode(FORMAT))
                name = socket.gethostbyaddr(addr[0])[0]
                pather = CURRENTDIR + "/received" +f"/{name}"
                foldercreator(name)

                msg_length2 = conn.recv(BYTESIZE).decode(FORMAT)
                
                if msg_length2:
                    msg_length2 = int(msg_length2)
                    filename = conn.recv(msg_length2).decode(FORMAT)
                    conn.send("Filename received".encode(FORMAT))

                    fullpath = pather +f"/{filename}"

                    msg_length3 = conn.recv(BYTESIZE).decode(FORMAT)

                    if msg_length3:
                            msg_length3 = int(msg_length3)
                            content = conn.recv(msg_length3)
                    

                            # while checksum != checksumrec:
                            #     conn.send("REQ".encode(FORMAT))
                            #     content = conn.recv(msg_length4)
                            #     checksum = calculate_checksum(content)
                            #     print(checksum)
                                


                            conn.send("File content received".encode(FORMAT))
                            writer(fullpath, content)
                            clear_buffer(conn, msg_length3)



                                
                

                        


            
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
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

def writer(path, content):
    file = open(path, "wb")
    file.write(content)
    file.close()

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