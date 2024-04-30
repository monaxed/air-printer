import socket
import os
import hashlib

BYTESIZE = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.11"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (BYTESIZE - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def sendcontent(file):
    filer = open(file, "rb")
    content = filer.read()
    filer.close()

    # Calculate checksum
    checksum = hashlib.md5(content).hexdigest()

    length = len(content)
    length = str(length).encode(FORMAT)
    length += b' ' * (BYTESIZE - len(length))

    # Send metadata (file type, file name, length, and checksum)
    send("application/pdf")
    send(os.path.basename(file))
    send(str(length))
    send(checksum)

    # Send file content
    client.send(content)
    print(client.recv(2048).decode(FORMAT))
    send(DISCONNECT_MESSAGE)

sendcontent("C:/Programming/Server/tester.pdf")
