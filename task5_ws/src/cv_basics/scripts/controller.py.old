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


################### IMPORT MODULES #######################

import rospy
import signal		# To handle Signals by OS/user
import sys		# To handle Signals by OS/user

# Message type used for publishing force vectors
from geometry_msgs.msg import Wrench
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

# u1 =fronty
# Message type used for receiving goals
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose2D		# Message type used for receiving feedback

import time
import math		# If you find it useful

from tf.transformations import euler_from_quaternion  # Convert angles

DMAX = 10000
stopped = False
mspeed = 300

x = 0
y = 0
theta = 0

xstop = False
ystop = False
tstop = True

pi = 3.14
curr = 0  # current position
maxgs = 0
x_goals = []
y_goals = []
theta_goals = []  # destination params

err = {'x': 0, 'y': 0, 't': 0}
aerr = {'x': 5, 'y': 5, 't': 0.016}  # accepted error

# why use this
damp = 5  # linear dampening factor
adamp = 1  # angular dampeneing factor

# a callback function for subscribing to /odom.
# this function will be automatically called everytime to update the pose of the robot
# (whenever there is an update in the /odom topic)

sastapi = 2*pi + 0.02


def conv(e):
    if e > 0 and e < pi:
        return e
    elif e > pi and e < sastapi:
        return -(pi - (e - pi))
    else:
        return e


def sign(a, x):
    if x >= 0:
        return abs(a)
    else:
        return -abs(a)

################## GLOBAL VARIABLES ######################


PI = 3.14


right_wheel_pub = None
left_wheel_pub = None
front_wheel_pub = None


##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code

def signal_handler(sig, frame):

    # NOTE: This function is called when a program is terminated by "Ctr+C" i.e. SIGINT signal
    # print('Clean-up !')
    cleanup()
    sys.exit(0)


def cleanup():
    vel = Vector3()

    v = Wrench()
    vel.x = 0
    vel.y = 0
    vel.z = 0
    v.force = vel
    right_wheel_pub.publish(v)
    front_wheel_pub.publish(v)
    left_wheel_pub.publish(v)
    ############ ADD YOUR CODE HERE ############

    # INSTRUCTIONS & HELP :
    # -> Not mandatory - but it is recommended to do some cleanup over here,
    # to make sure that your logic and the robot model behaves predictably in the next run.

    ############################################


def task2_goals_Cb(msg):
    global x_goals, y_goals, theta_goals, maxgs
    # print("IN HHERREE")

    x_goals.clear()
    y_goals.clear()
    theta_goals.clear()

    for waypoint_pose in msg.poses:
        x_goals.append(waypoint_pose.position.x)
        y_goals.append(waypoint_pose.position.y)

        orientation_q = waypoint_pose.orientation
        orientation_list = [orientation_q.x,
                            orientation_q.y, orientation_q.z, orientation_q.w]
        theta_goal = euler_from_quaternion(orientation_list)[2]
        theta_goals.append(theta_goal)

    maxgs = len(x_goals)
    # print("I EXIT")


def aruco_feedback_Cb(data):
    global x, y, theta, err, maxgs
    if maxgs == 0:
        return
    # print(data.theta)
    pos = data

    x = pos.x
    y = pos.y
    # print("x, y = ", x, y)
    err['x'] = x_goals[curr] - pos.x
    err['x'] *= 1
    err['y'] = y_goals[curr] - pos.y
    err['y'] *= 1

    _theta = pos.theta
    theta = _theta

    err['t'] = ((theta_goals[curr]) - pos.theta) % (2*pi)
    if err['t'] > pi:
        err['t'] = -(2*pi - err['t'])
    print("--------------------------", err['t'])
    # print(curr, err)
    ############ ADD YOUR CODE HERE ############

    # INSTRUCTIONS & HELP :
    # -> Receive & store the feedback / coordinates found by aruco detection logic.
    # -> This feedback plays the same role as the 'Odometry' did in the previous task.

    ############################################


def waitandreset():
    global stopped, xstop, ystop, tstop
    stopped = True
    rospy.sleep(2)
    stopped = False
    xstop = ystop = False
    tstop = True
    # how to turn while moving


def pub_fvel(vel):
    d = 1
    w_bz = vel.angular.z
    v_bx = vel.linear.x
    v_by = -vel.linear.y
    # print("vy = ", v_by)
    # print("err - ", err['x'], err['y'])
    # print("vel = ", v_bx, v_by)
    uf = (-d*w_bz)+v_bx
    ur = (-d*w_bz)+(-0.5*v_bx)+(-0.866*v_by)
    ul = (-d*w_bz)+(-0.5*v_bx)+(0.866*v_by)
    # print("uuuu -  ", uf, ul, ur)

    # 0, uf
    tmp = Wrench()
    tmptmp = Vector3()
    tmptmp.x = uf
    tmp.force = tmptmp
    uf = tmp
    # print("ff - ", tmptmp.x, tmptmp.y)

    # ur * cos(-30), ur * sin(-30)
    tmp = Wrench()
    tmptmp = Vector3()
    tmptmp.x = ur
    tmp.force = tmptmp
    ur = tmp
    # print("fr - ", tmptmp.x, tmptmp.y)

    # ul * cos(-150), ul * sin(-150)
    tmp = Wrench()
    tmptmp = Vector3()
    tmptmp.x = ul
    tmp.force = tmptmp
    ul = tmp
    # print("fl - ", tmptmp.x, tmptmp.y)

    right_wheel_pub.publish(ur)
    left_wheel_pub.publish(ul)
    front_wheel_pub.publish(uf)


def inverse_kinematics():
    pass
    ############ ADD YOUR CODE HERE ############

    # INSTRUCTIONS & HELP :sign(10, e)


def stoprob():
    right_wheel_pub.publish(Wrench())
    left_wheel_pub.publish(Wrench())
    front_wheel_pub.publish(Wrench())


def main():

    global err, curr, xstop, ystop, tstop, flag, theta, maxgs, right_wheel_pub, left_wheel_pub, front_wheel_pub
    curr = 0
    rospy.init_node('controller_node')

    signal.signal(signal.SIGINT, signal_handler)

    # NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
    # Use the below given topics to generate motion for the robot.
    right_wheel_pub = rospy.Publisher(
        '/right_wheel_force', Wrench, queue_size=10)
    front_wheel_pub = rospy.Publisher(
        '/front_wheel_force', Wrench, queue_size=10)
    left_wheel_pub = rospy.Publisher(
        '/left_wheel_force', Wrench, queue_size=10)

    rospy.Subscriber('detected_aruco', Pose2D, aruco_feedback_Cb)
    rospy.Subscriber('task2_goals', PoseArray, task2_goals_Cb)

    rate = rospy.Rate(50)

    ############ ADD YOUR CODE HERE ############

    # INSTRUCTIONS & HELP :
    # -> Make use of the logic you have developed in previous task to go-to-goal.
    # -> Extend your logic to handle the feedback that is in terms of pixels.
    # -> Tune your controller accordingly.
    # 	-> In this task you have to further implement (Inverse Kinematics!)
    #      find three omni-wheel velocities (v1, v2, v3) = left/right/center_wheel_force (assumption to simplify)
    #      given velocity of the chassis (Vx, Vy, W)
    #
    while (maxgs == 0):
        pass
    rospy.sleep(1)

    while not rospy.is_shutdown():
        vel = Twist()
        if (abs(err['x']) < aerr['x']):  # stop if the error is within range
            vel.linear.x = 0
            xstop = True

        if (abs(err['y']) < aerr['y']):  # same as above
            vel.linear.y = 0
            ystop = True
        #print("errbfr :- ", err['x'], err['y'], err['t'])
        if (xstop and ystop):
            if (abs(err['t']) < aerr['t']):
                vel.angular.z = 0
                # pub_c.publish(vel)
                # this vel will ap;ways be zero
                stoprob()
                tstop = True
                #print("%d is done now waiting!" % curr)
                if curr < maxgs-1:
                    curr += 1
                waitandreset()
            else:
                e = err['t']
                #print("---------eeeeeee---------", err['t'])
                e = conv(e)

                vel.linear.x = 0
                vel.linear.y = 0
                vel.angular.z = sign(15, -e)
                print("==============", vel.angular.z)
                tstop = False

        if tstop:
            vx = err['x']*damp
            vy = err['y']*damp
            ##print(vx, vy)
            ##print(err['x'], err['y'])
            if abs(vx) < aerr['x']:
                vx = 0
                vy = sign(1, vy)
            else:
                aa = math.atan(vy/vx)
                vx = sign(math.cos(aa), vx)
                vy = sign(math.sin(aa), vy)
            #print("errbfr :- ", err['x'], err['y'], err['t'])
            #print("velbrr :- ", vx, vy)
            vel.linear.x = mspeed * (vx *
                                     math.cos(-theta) - vy * math.sin(-theta))
            vel.linear.y = mspeed * (vx *
                                     math.sin(-theta) + vy * math.cos(-theta))
            vel.angular.z = 0
            xstop = False
            ystop = False
            tstop = True

        # Calculate Error from feedback
            #print("vell - ", vel.linear.x, vel.linear.y, theta)
        pub_fvel(vel)
        # Change the frame by using Rotation Matrix (If you find it required)

        # Calculate the required velocity of bot for the next iteration(s)

        # Find the required force vectors for individual wheels from it.(Inverse Kinematics)

        # Apply appropriate force vectors

        # Modify the condition to Switch to Next goal (given position in pixels instead of meters)

        rate.sleep()

    ############################################


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
