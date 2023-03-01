import sys
import datetime
import numpy as np
import cv2
import cv2.aruco as aruco
import math
from math import pi
import threading
import traceback
import controller
from time import sleep

ARENABORDERIDS = [2, 4, 8, 10]
ROBOT = 15
RES = (1024, 1280)
'''
camera_matrix = np.array([1036.831939802416, 0, 655.0302317554891, 0, 1031.833145877669, 559.8336241002479, 0, 0, 1], dtype = np.float32)
camera_matrix = camera_matrix.reshape((3, 3))
dist_coeffs = np.array([-0.337507, 0.080140, -0.010452, 0.0129054, 0.000000],dtype = np.float32)
'''
camera_matrix = np.array( [1036.831939802416, 0, 655.0302317554891, 0, 1031.833145877669, 559.8336241002479, 0, 0, 1]   , dtype = np.float32)
camera_matrix = camera_matrix.reshape((3, 3))                                                                                                
dist_coeffs = np.array([-0.4609349180840622, 0.1672658106558054, -0.006744359326849965, -0.001268283627654576, 0],dtype = np.float32)        
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

(ocx, ocy) = (0, 0)#coods according to opencv
(fakex,fakey) = (0, 0)
(cx, cy, theta) =  (-1, -1, 0)#coords according to problem
cap = None
cw, ch = 1, 1

scoods = [0, 0, 0, 0]#stabilized coordinates
stol = 5#px stabillization tolerance
sTol = 200#High tolerance point

def stabilizebounds(r):
    global scoods
    for i in range(4):
        if abs(r[i]-scoods[i])>=sTol:
            scoods[i] = r[i]
        elif abs(r[i]-scoods[i])>=stol:
            r[i] = scoods[i]
            scoods[i] = r[i]-stol

    
def addtheta(a, b): 
    return (-a-b+pi)%(2*pi) - pi

def get_centroid(corn_pts):
    global cx, cy, ocx, ocy, fakex, fakey
    corn_pts = corn_pts[0]
    M = cv2.moments(corn_pts)
    # might convert to int??
    cent_x = ((M["m10"] / M["m00"]))
    cent_y = ((M["m01"] / M["m00"]))
    ocx, ocy = (int(cent_x), int(cent_y))
    (cx, cy) = (int(cent_x), ch-int(cent_y))#flipping y axis
    (fakex, fakey) = (cx/cw * 500, 500 - cy/ch * 500)

def get_theta(corn_pts):
    global ocx, ocy, theta
    get_centroid(corn_pts)
    cX, cY = ocx, ocy
    corn_ptsi = np.squeeze(corn_pts[0])
    bX = corn_ptsi[1][0]
    bY = corn_ptsi[1][1]
    x_diff = bX - cX
    y_diff = bY - cY
    #print("DIFF, ", x_diff, y_diff)
    ans_1 = math.atan2(y_diff, x_diff)
    ret = (ans_1 + math.pi/4) % (2*math.pi)
    if ret > math.pi:
        ret = -(2*math.pi - ret)
    theta = ret

def image_mode():
    # @param:   None
    # @return:  Contour coordinates as numpy array
    
    # read the snapchat logo image 
    img = cv2.imread("../taskImages/snapchat.png")
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resizing the image to 500, 500
    img_resized = cv2.resize(img_grey, (500, 500))
    # testing if properly resized
    print(img_resized.shape)
    
    assert img_resized.shape == (500, 500)
    # getting the edges of the shape
    edges = cv2.Canny(img_resized, 30, 200)
    # getting the contour coordinates
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
    contours = list(contours)
    # print(contours)
    a = [(list(x)[0][0], list(x)[0][1]) for x in contours]
    final = [s for s in a if a.index(s) % 4 == 0]
    # print(type(a[0]))
    # print(final)
    # print(a)
    return final

def callback(current_frame):
    global cw, ch
    (corners, ids, _) = detector.detectMarkers(current_frame)
    
    try:
        corners = np.array(corners).reshape((-1, 2))
        rect = cv2.boundingRect(corners)
        #rect = list(rect)
        #print(rect)
        #stabilizebounds(rect)
        #rect = scoods
        #print(rect)
        cropped = current_frame[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        cw, ch = rect[2], rect[3]
        cropped = cv2.flip(cropped, -1)

        (corners, ids, _) = detector.detectMarkers(cropped)
        
        ids = [i[0] for i in ids]
        arucos=dict(zip(ids, corners))
        if 15 in ids:
            get_centroid(arucos[15])
            get_theta(arucos[15])

        controller.setcoods(cx, cy, theta)
        cv2.putText(cropped, "{} {} {}({})".format(int(fakex), int(fakey), round(theta, 5), round(theta*180/pi)),\
                    (10,250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("1", cropped)
        #Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return
    except KeyboardInterrupt as e:
        controller.STOP = True
        controller.STOPREASON = "keyboard interrupt"
        sleep(1)

    except Exception as e:
        print(traceback.format_exc())
        arucos = ()
    #print(arucos)

def setcamera():
    global cap
    print(sys.argv)
    if len(sys.argv) <= 1:
        cap = cv2.VideoCapture("/dev/video2")
    else:
        print(908)
        cap = cv2.VideoCapture(int(sys.argv[1]))

    codec = 0x47504A4D  # MPG
    cap.set(cv2.CAP_PROP_FOURCC, codec)
    cap.set(cv2.CAP_PROP_FPS, 60.0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

def setgoals(a):
    ngoals = []
    for i in a:
        q = int(i[0]/500.0 * cw)
        b = int(i[1]/500.0 * ch)
        ngoals.append((q, b, 0))
    print(ngoals)
    controller.setgoals(ngoals)

def get_coods():
    # Open the video capture
    gotot = threading.Thread(target=controller.goto, args=())
    gotot.start()
    while True:
        try:
        # Capture the frame from the video feed
            ret, frame = cap.read()
            if not ret:
                print("prob with cam")
                break
            h, w = frame.shape[:2]
            #print("h, w, {}, {}", h, w)
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)

            callback(frame)

            if not controller.aregoalsset():
                #setgoals([(250, 250, 0), (250, 250, pi/2), (250, 250, pi)])
                setgoals([(250, 250, 0), (350, 300, pi/4), (150, 300, 3*pi/4), (150, 150, -3*pi/4), (350, 150, -pi/4)])
                # setgoals(image_mode())
            controller.geterr(cx, cy, theta)
            #print(controller.currx, controller.curry)
            #print("ERROR", controller.errx, controller.erry)
            #print(controller.currvel)
        except KeyboardInterrupt as e:
            controller.STOP = True
            controller.STOPREASON = "keyboard interrupt"
            sleep(1)
            exit()
        except Exception as e:
            print(traceback.format_exc())
        
    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setcamera()
    addr = controller.connect()
    get_coods()

    #print("Connected at addr - {}".format(addr))
