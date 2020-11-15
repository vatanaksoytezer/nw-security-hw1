import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65437        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    s.sendall(b"Hello from client")
    data = s.recv(1024)
    msg = data.decode("utf-8")
    if msg  == "10":
        break
    print("Received: ", repr(msg))
    time.sleep(0.5)

