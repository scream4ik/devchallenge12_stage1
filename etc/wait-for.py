# https://stackoverflow.com/a/35841740
import socket
import time

host = 'postgres'
port = 5432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)
