import numpy as np
import cv2
import cv2.aruco as aruco
import math
from threading import Thread

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



def get_centroid(corn_pts):
    corn_pts = corn_pts[0]
    M = cv2.moments(corn_pts)
    # might convert to int??
    cent_x = ((M["m10"] / M["m00"]))
    cent_y = ((M["m01"] / M["m00"]))
    return (cent_x, cent_y)


def get_theta(corn_pts):
    cX, cY = get_centroid(corn_pts)
    corn_ptsi = np.squeeze(corn_pts[0])
    bX = corn_ptsi[1][0]
    bY = corn_ptsi[1][1]
    x_diff = bX - cX
    y_diff = bY - cY
    ans_1 = math.atan2(y_diff, x_diff)
    ret = (ans_1 + math.pi/4) % (2*math.pi)
    if ret > math.pi:
        ret = -(2*math.pi - ret)
    return ret


def callback(current_frame):

    (corners, ids, _) = detector.detectMarkers(current_frame)
    # print(len(corners))
    # print(np.squeeze(corners[0])[0][0])
    try:
        arucos=()
        #arucos = dict(zip(ids, corners))
        #for (i, id) in enumerate(ARENABORDERIDS):
         #   corners = arucos[id]
          #  arenacornpts[i] = get_centroid(corners)
            #arenamask = np.zeros(RES, np.unit8)
            #arenamask = cv2.drawContours(arenamask, [[arenacornpts]], -1, (255, 255, 255), cv2.LINE_AA)
        corners = np.array(corners).reshape((-1, 2))
        #rect = cv2.boundingRect(corners)
        mask = np.zeros(current_frame.shape[:2])
        for i in corners:
            mask[i
                 ] 
        #cropped = current_frame[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        cv2.drawContours(current_frame, hull, 0, (255, 0, 0), 8)
        #wbg = np.ones_like(img, np.uint8)*255
        #print(wbg.shape[:2])
        #wbg = cv2.bitwise_not(wbg, mask=arenamask)

        #cropped = wbg + cropped
        cv2.imshow("Aruco markers", current_frame)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return
        
    except Exception as e:
        print(e)
        arucos = ()
    print(arucos)

def main():
    # Open the video capture
    cap = cv2.VideoCapture("/dev/video2")
    codec = 0x47504A4D  # MJPG
    cap.set(cv2.CAP_PROP_FPS, 30.0)
    cap.set(cv2.CAP_PROP_FOURCC, codec)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

    while True:
        # Capture the frame from the video feed
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        print("h, w, {}, {}", h, w)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
        frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)

        callback(frame)
                
        '''        cv2.imshow("Aruco markers", new_frame)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break '''

    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

    

if __name__ == '__main__':
    main()
