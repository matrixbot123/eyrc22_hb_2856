import datetime
import numpy as np
import cv2
import cv2.aruco as aruco
import math
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

pi = 3.1415
(cx, cy, theta) =  (-1, -1, 0)
cap = None

def get_centroid(corn_pts):
    global cx, cy
    corn_pts = corn_pts[0]
    M = cv2.moments(corn_pts)
    # might convert to int??
    cent_x = ((M["m10"] / M["m00"]))
    cent_y = ((M["m01"] / M["m00"]))
    (cx, cy) = (int(cent_x), int(cent_y))

def get_theta(corn_pts):
    global cx, cy, theta
    get_centroid(corn_pts)
    cX, cY = cx, cy
    corn_ptsi = np.squeeze(corn_pts[0])
    bX = corn_ptsi[1][0]
    bY = corn_ptsi[1][1]
    x_diff = bX - cX
    y_diff = bY - cY
    ans_1 = math.atan2(y_diff, x_diff)
    ret = (ans_1 + math.pi/4) % (2*math.pi)
    if ret > math.pi:
        ret = -(2*math.pi - ret)
    theta = ret


def callback(current_frame):
    (corners, ids, _) = detector.detectMarkers(current_frame)
    # print(len(corners))
    # print(np.squeeze(corners[0])[0][0])
    try:
        corners = np.array(corners).reshape((-1, 2))
        rect = cv2.boundingRect(corners)
        cropped = current_frame[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        cropped = cv2.resize(cropped, (500, 500))
        (corners, ids, _) = detector.detectMarkers(cropped)
        
        ids = [i[0] for i in ids]
        arucos=dict(zip(ids, corners))
        if 15 in ids:
            #print(arucos)
            #print(ids, arucos[15][0])
            get_theta(arucos[15])
            get_centroid(arucos[15])
            
        cv2.putText(cropped, "{} {} {}".format(int(cx), int(cy), theta),\
                    (10,250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        if cx!=-1 and cy!=-1:
            cv2.arrowedLine(cropped, (cx, cy),
                            (int(cx+controller.currvel[0]/7), int(cy+controller.currvel[1]/7)),
                            (0, 0, 255), 4)
        cv2.imshow("Aruco markers", cropped)
        #Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return
    except KeyboardInterrupt as e:
        controller.STOP = True
        sleep(1)

    except Exception as e:
        print(traceback.format_exc())
        arucos = ()
    #print(arucos)

def setcamera():
    global cap
    cap = cv2.VideoCapture("/dev/video2")
    codec = 0x47504A4D  # MJPG
    cap.set(cv2.CAP_PROP_FPS, 30.0)
    cap.set(cv2.CAP_PROP_FOURCC, codec)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

def get_coods():
    # Open the video capture
    gotot = threading.Thread(target=controller.goto, args=())
    gotot.start()
    while True:
        try:
        # Capture the frame from the video feed
            ret, frame = cap.read()
            if not ret:
                break
            h, w = frame.shape[:2]
            #print("h, w, {}, {}", h, w)
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)

            callback(frame)

            controller.geterr(cx, cy, theta)
            #print(controller.currx, controller.curry)
            print("ERROR", controller.errx, controller.erry)
            #print(controller.currvel)
        except KeyboardInterrupt as e:
            controller.STOP = True
            sleep(1)
            exit()
        except Exception as e:
            print(traceback.format_exc())
        
    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setcamera()
    #addr = controller.connect()
    controller.setgoals([(250, 250, 0)])
    get_coods()
    print("Connected at addr - {}".format(addr))
