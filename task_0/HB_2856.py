#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_0.py
# Functions:
# 					[ Comma separated list of functions in this file ]
# Nodes:		    Add your publishing and subscribing node


####################### IMPORT MODULES #######################
import sys
import traceback
from geometry_msgs.msg import Twist
import math
import rospy
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, atan
import time
##############################################################


def callback(x):
    rospy.loginfo("Data Received: %s", x.pose)


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.flag = True
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)
        self.pose = Pose()
        self.origin = (5.5445, 5.5445)
        self.tolerance = 0.000039

        self.dist = 0

    def get_origin(self):
        self.origin = (self.pose.x, self.pose.y)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

        x = self.pose.x
        y = self.pose.y

        self.dist = math.sqrt(pow(x-self.origin[0], 2) +
                              pow(y-self.origin[1], 2))
        #print(self.pose.x, self.pose.y, self.pose.theta, self.dist)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # Get the input from the user.
        vel_msg = Twist()
        time.sleep(0.5)
        self.get_origin()
        print(self.pose)
        while abs(self.dist - 2) > self.tolerance:

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.

            vel_msg.linear.x = 1
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 1

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

    def rotate(self):
        req_theta = \
            atan((self.pose.y - self.origin[1])/(self.pose.x - self.origin[0]))
        print("required theta : "+str(req_theta))
        # input()

        vel_msg = Twist()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        # Angular velocity in the z-axis.
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 1

        while abs(self.pose.theta - req_theta) > 0.0025:
            print(self.pose.theta - req_theta)
            self.velocity_publisher.publish(vel_msg)
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        # Angular velocity in the z-axis.
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0

        # while abs(req_distance-)

        self.velocity_publisher.publish(vel_msg)

    def move2origin(self):

        # input()
        vel_msg = Twist()
        min = 1
        vel_msg.linear.x = 1
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        # Angular velocity in the z-axis.
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        while self.dist > 0.05:
            # if (self.dist < min):
            #     min = self.dist
            # print("self.dist"+str(self.dist))
            self.velocity_publisher.publish(vel_msg)
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)


def main():
    x = TurtleBot()
    x.move2goal()
    x.rotate()
    x.move2origin()


################# ADD GLOBAL VARIABLES HERE #################


##############################################################


################# ADD UTILITY FUNCTIONS HERE #################


##############################################################

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
