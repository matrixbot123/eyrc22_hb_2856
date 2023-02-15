import socket
from time import sleep
import signal		
import sys		

def signal_handler(sig, frame):
    print('Clean-up !')
    cleanup()
    sys.exit(0)

def cleanup():
    s.close()
    print("cleanup done")

ip = "192.168.29.247"     #Enter IP address of laptop after connecting it to WIFI hotspot


#We will be sending a simple counter which counts from 1 to 10 and then closes the socket
counter = 1

#To undeerstand the working of the code, visit https://docs.python.org/3/library/socket.html
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 8002))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            coods = input("->")
            coods += "\n"
            conn.sendall(str.encode(str(coods)))
            data = conn.recv(1024)
            print("data -> ", data)
