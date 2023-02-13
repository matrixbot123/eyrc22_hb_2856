#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (HB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:		[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:		feedback.py
# Functions:
# [ Comma separated list of functions in this file ]
# Nodes:		Add your publishing and subscribing node


######################## IMPORT MODULES ##########################

import numpy as np				# If you find it required
import rospy
from sensor_msgs.msg import Image 	# Image is the message type for images in ROS
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2				# OpenCV Library
import math				# If you find it required
# Required to publish ARUCO's detected position & orientation
from geometry_msgs.msg import Pose2D

############################ GLOBALS #############################

aruco_publisher = rospy.Publisher('detected_aruco', Pose2D)
aruco_msg = Pose2D()
rate = None
##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code


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


def callback(data):
    # Bridge is Used to Convert ROS Image message to OpenCV image
    br = CvBridge()
    rospy.loginfo("receiving camera frame")
    # Receiving raw image in a "grayscale" format
    get_frame = br.imgmsg_to_cv2(data, "mono8")
    current_frame = cv2.resize(
        get_frame, (500, 500), interpolation=cv2.INTER_LINEAR)

    ############ ADD YOUR CODE HERE ############

    # INSTRUCTIONS & HELP :
    # -> Use OpenCV to find ARUCO MARKER from the IMAGE
    # -> You are allowed to use any other library for ARUCO detection,
    #        but the code should be strictly written by your team and
    # your code should take image & publish coordinates on the topics as specified only.
    # -> Use basic high-school geometry of "TRAPEZOIDAL SHAPES" to find accurate marker coordinates & orientation :)
    # -> Observe the accuracy of aruco detection & handle every possible corner cases to get maximum scores !

    ############################################
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    aruco_parameters = cv2.aruco.DetectorParameters_create()
    # rishi changed here
    (corners) = cv2.aruco.detectMarkers(
        current_frame, aruco_dict, parameters=aruco_parameters)[0]
    # print(len(corners))
    # print(np.squeeze(corners[0])[0][0])
    print(get_theta(corners.copy()))
    #print(int(tmp[0]), int(tmp[1]), get_theta(corners.copy()))
    ret = Pose2D()
    ret.x = get_centroid(corners.copy())[0]
    ret.y = get_centroid(corners.copy())[1]
    ret.theta = get_theta(corners.copy())
    # print(ret.theta)
    aruco_publisher.publish(ret)


def main():
    global rate
    rospy.init_node('aruco_feedback_node')
    rate = rospy.Rate(300)
    rospy.Subscriber('overhead_cam/image_raw', Image, callback)

    rospy.spin()


if __name__ == '__main__':
    main()
