import hashlib
import socket
import threading
import os

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
    print(f"[NEW CONNECTION] {addr} connected")
    pather = ""

    connected = True
    while connected:
        msg_length_bytes = conn.recv(BYTESIZE)
        if msg_length_bytes:
            msg_length = int.from_bytes(msg_length_bytes, "big")  # Convert bytes to integer
            msg = conn.recv(msg_length)
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
            
            if msg == b"application/pdf":
                conn.send("PDF file type received".encode(FORMAT))
                name = socket.gethostbyaddr(addr[0])[0]
                pather = CURRENTDIR + "/received" +f"/{name}"
                foldercreator(name)

                msg_length2_bytes = conn.recv(BYTESIZE)
                
                if msg_length2_bytes:
                    msg_length2 = int.from_bytes(msg_length2_bytes, "big")  # Convert bytes to integer
                    filename = conn.recv(msg_length2)
                    conn.send("Filename received".encode(FORMAT))

                    fullpath = pather +f"/{filename.decode(FORMAT)}"

                    msg_length3_bytes = conn.recv(BYTESIZE)

                    if msg_length3_bytes:
                        msg_length3 = int.from_bytes(msg_length3_bytes, "big")  # Convert bytes to integer
                        content = b""  # Initialize content as an empty byte string

                        # Receive content until it reaches the expected length
                        remaining_length = msg_length3
                        while remaining_length > 0:
                            data = conn.recv(min(BYTESIZE, remaining_length))
                            if not data:
                                break
                            content += data
                            remaining_length -= len(data)
                        
                        # Calculate checksum of received content
                        checksum = calculate_checksum(content)

                        conn.send("File content received".encode(FORMAT))

                        # Verify checksum
                        checksum_received = conn.recv(BYTESIZE).decode(FORMAT)
                        if checksum_received == checksum:
                            writer(fullpath, content)
                            print("[INFO] File successfully received and saved.")
                        else:
                            print("[ERROR] Checksum verification failed. Data may be corrupted.")
                            # Handle checksum verification failure
                            # For example, request retransmission of the file
                        
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
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
    with open(path, "wb") as file:
        file.write(content)

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

print("[STARTING] server is starting....") 
start()
