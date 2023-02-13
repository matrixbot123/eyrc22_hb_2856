import threading, datetime

currvel = (0, 0, 0)
currxy = (0, 0)
currgoal = (0, 0)
nextgoals = []#stack of next goals

aerror = [20, 20]#accepted error

def broadcastvel(conn):
    while True:
        data = currvel[0] + " " + currvel[1] + " " currvel[2] + "\n"
        conn.sendall(str.encode(data))
        data = conn.recv(1024)
        if int(data) == 1:
            print("Successfully transmitted at "
                  + str(datetime.datetime.now()))

def getcoods():
    while True:
        currxy = (0, 0)

def goto(coods):
    while True:
        if 
    
def main():
    ip = "192.168.29.247"     #Enter IP address of laptop after connecting it to WIFI hotspot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 8002))
    s.listen()
    conn, addr = s.accept()
    
    broadcast = threading.Thread(target = broacdcastvel, args = (conn, ))
    getcoods = threading.Thread(target = getcoods, args = ())
    goto = threading.Thread(target = goto, args = ())

    broadcast.start()
    getcoods.start()
