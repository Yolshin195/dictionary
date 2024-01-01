import socket
import time
import os

host = os.environ["DB_HOST"]
port = int(os.environ["DB_PORT"])

print(f"Begin waiting postgres on {host}:{port}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)

print(f"End waiting postgres on {host}:{port}")
