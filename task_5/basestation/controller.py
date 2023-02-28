import math
import threading, datetime
import feedback
import socket
from time import sleep
from math import pi, e, pow

#constants
VCONSTX = 100
VCONSTY = -100
VCONSTZ = -50

#--non constants
STOP = False#emergency stop flag
STOPREASON=""


currvel = (0, 0, 0)
currx, curry, theta = (0, 0, 0)
errx, erry, errt = (0, 0 ,0)
goalx, goaly, goalt = (0, 0, 0)
nextgoals = []#stack of next goals
conn=None
aerrorx, aerrory, aerrort = 3, 3, 0.015#accepted error
check = 0
#-------------------
#helper functions

def sign(a, x):
    if x >= 0:
        return abs(a)
    else:
        return -abs(a)

#-------------------

def norm(a, b):
    m = max(abs(a), abs(b))
    if m == 0:
        return
    return (a/m, b/m)

def setgoals(goals):
    global nextgoals, goalx, goaly, goalt
    goalx, goaly, goalt = goals.pop(0)
    print("Going to Origin Pose.")
    nextgoals = goals

def aregoalsset():
    if len(nextgoals) == 0 and goalx==0 and goaly==0:
        return False
    else:
        return True

def broadcastvel(conn):
    if STOP:
        data = "0 0 0\n"
        #print("STOPPING for "+STOPREASON)
        conn.sendall(str.encode(data))
        data = conn.recv(1024).decode()
        return
    data = str(currvel[0]) + " " + str(currvel[1]) + " " + str(currvel[2]) + "\n"
    #print(data)
    conn.sendall(str.encode(data))
    ret = conn.recv(1024).decode()
    if int(ret) == 1:
        pass
        #print("Successfully transmitted {} at {} ".format(data, str(datetime.datetime.now())))


def setcoods(cx, cy, t):
    global currx, curry, theta
    currx, curry, theta = cx, cy, t

def geterr(currx, curry, theta):
    global errx, erry, errt
    (errx, erry, errt) = goalx - currx, goaly - curry, goalt - theta
    #print(errt)

def pause(t, reason):#pauses robot for t s
    global conn, STOP, STOPREASON
    #print(reason)
    SROPREASON=reason
    STOP=True
    broadcastvel(conn)
    sleep(t)
    STOP=False

def sigmoid(a):
    a = a*180/pi
    return VCONSTZ * 1.8/(1 + 17 * pow(e, -a))

def goto():
    global goalx, goaly, goalt, errx, erry, currvel, STOP, STOPREASON, check
    sleep(2)
    
    while True:
        ex, ey, et = 0, 0, 0
        velx, vely, velz = (0, 0, 0)
        if abs(errx)<aerrorx and abs(erry)<aerrory:#if reached linear goal
            #print("Stopped linearly")
            #pause(1, "Stopped Linearly")
            if abs(errt)<aerrort:
#                print(theta, errt)
                if len(nextgoals)==0:
                    STOP = True
                    STOPREASON = "DONE"
                    broadcastvel(conn)
                    print("Done.")
                    exit()
                else:
                    (goalx, goaly, goalt) = nextgoals.pop(0)
                print("GOAL REACHED")
                pause(3, "One goal done")
                continue
            else:
                velz = 0
                thetatmp = theta+pi
                goalttmp = goalt+pi
                if abs(goalttmp - thetatmp)<pi:
                    velz = sign(sigmoid(abs(errt)), goalttmp-thetatmp)
                else:
                    velz = -sign(sigmoid(abs(errt)), goalttmp-thetatmp)
                currvel = (0, 0, velz)
                broadcastvel(conn)
        else:
            if errx==0:
                    ex = 0
                    ey = sign(1, erry)
            else:
                    aa = math.atan(erry/errx)
                    ex = sign(math.cos(aa), errx)
                    ey = sign(math.sin(aa), erry)

            (ex, ey) = norm(errx, erry)
            velx = VCONSTX * (ex * math.cos(theta) - ey * math.sin(theta))
            vely = VCONSTY * (ex * math.sin(theta) + ey * math.cos(theta))
            #print("ERR ____", errx, erry, theta)
            #print("VELOCITY ___ ", velx, vely)
            #print("Publishing vel {}, {}".format(velx, vely))

            currvel = (velx, vely, 0)
            #print("currvel", currvel)
        broadcastvel(conn)

def connect():
    global conn
    
    ip = "192.168.29.247"     #Enter IP address of laptop after connecting it to WIFI hotspot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 8005))
    s.listen()
    conn, addr = s.accept()
    return addr
