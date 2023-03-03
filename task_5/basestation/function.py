import math
import numpy as np

pi = math.pi

def lissajous(t):
    x = 200 * math.cos(t)
    y = 100 * math.sin(2*t)
    theta = (np.pi / 4) * math.sin(t)
    return (x, y, theta)

def getgoals():
    thetas = np.linspace(0, 2*np.pi, 1000)
    points = []
    for i in thetas:
        x, y, th = lissajous(i)
        points.append((int(x)+250, int(y)+250 , th))
    
    return points

