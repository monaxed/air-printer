import hashlib
import socket
import threading
import os
import sys
import time
import PrintingSRC as printer
import fileClass 

BYTESIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DSICONNECT"

CURRENTDIR = os.getcwd()
QUE = [] #global print queue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#To handle main print queue coming from various device
def printque():
    global QUE

    while True:
        if len(QUE) !=0:
            for i in QUE:
                i.sendprintjob()
                QUE.pop(QUE.index(i))


def handle_client(conn, addr):
    global QUE


    print("")
    print(f"[NEW CONNECTION] {addr}  connected")
    pather = ""
    connected = True
    devicename = socket.gethostbyaddr(addr[0])[0]

    while connected:

        msg = conn.recv(1024).decode()
        if msg == DISCONNECT_MESSAGE or msg == "":
            connected = False
        
        if msg == "application/pdf":
            print(f"[SERVER STATUS] Received file type of {msg} --> FROM [{devicename}]")
            name = conn.recv(1024).decode()
            print(f"[SERVER STATUS] File name received as {name} --> FROM [{devicename}]")
            # conn.send("name received".encode(FORMAT))
            pather = foldercreator(devicename)
            
            content = b""
            done = False
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                content += data
                if content.endswith(b"<END>"):
                    break


                
            conn.send("File content received".encode(FORMAT))
            path = pather + f"/{name}"
            writer(path, content, devicename)
            clear_buffer(conn, len(content))
            newprintjob = fileClass.filer(devicename, path) #sent file is packed into a class, which then will be printed from the class

            QUE.append(newprintjob) #global print queue
            #printer.calltoprint(path, devicename)

            print("")
            
    conn.close()
    print(f"[SERVER STATUS] {devicename} DISCONNECTED!")
    
    

def start():
    server.listen()
    print(f"[LISTENING] listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args =(conn, addr))
        thread2 = threading.Thread(target = printque)
        thread.start()
        thread2.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
    

def foldercreator(devicename):
    path2 = CURRENTDIR + "/received"
    if os.path.exists(path2):
        path2 = path2 + f"/{devicename}"

        if not os.path.exists(path2):
            os.makedirs(path2)
            os.chmod(path2, 0o777)
            #pather = path2
            return path2
        else:
            return path2

    else:
        dir = path2 + f"/{devicename}"
        os.makedirs(dir)
        os.chmod(dir, 0o777)
        return dir



def writer(path, content, user):
    print(path)
    file = open(path, "wb")
    os.chmod(path, 0o666)
    file.write(content)
    file.close()
    print(f"[RECEIVER] File has been received succesfully --> FROM {user}")

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