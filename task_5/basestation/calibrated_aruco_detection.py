
import numpy as np
import cv2
import cv2.aruco as aruco


def set_res(cap, x,y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

camera_matrix = np.array( [1036.831939802416, 0, 655.0302317554891, 0, 1031.833145877669, 559.8336241002479, 0, 0, 1]   , dtype = np.float32)
camera_matrix = camera_matrix.reshape((3, 3))
dist_coeffs = np.array([-0.4609349180840622, 0.1672658106558054, -0.006744359326849965, -0.001268283627654576, 0],dtype = np.float32)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

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
    print(f"height {h} and and width {w}") 
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
    new_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)
    gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    print(corners)
    frame = aruco.drawDetectedMarkers(new_frame, corners, ids)

    # Display the frame
    cv2.imshow("Aruco markers", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()
cv2.destroyAllWindows()
