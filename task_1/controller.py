#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseArray
# publishing to /cmd_vel with msg type: Twist
from geometry_msgs.msg import Twist
# subscribing to /odom with msg type: Odometry
from nav_msgs.msg import Odometry

# for finding sin() cos() 
import math

# Odometry is given as a quaternion, but for the controller we'll need to find the orientaion theta by converting to euler angle
from tf.transformations import euler_from_quaternion

DMAX = 10000
stopped = False
mspeed = 1

x = 0
y = 0
theta = 0

xstop = False
ystop = False
tstop = True

pi = 3.14
curr = 0#current position
maxgs = 0
x_goals =     [ ]
y_goals =     [ ]
theta_goals = [ ]#destination params

err = {'x': 0, 'y' : 0, 't':0}
aerr = {'x': 0.01, 'y' : 0.01, 't':0.001}#accepted error

damp=5#linear dampening factor
adamp=10#angular dampeneing factor

# a callback function for subscribing to /odom. 
# this function will be automatically called everytime to update the pose of the robot 
# (whenever there is an update in the /odom topic)

def sign(a, x):
    if x>=0:
        return abs(a)
    else:
        return -abs(a)

def geterror(data):
    global x, y, theta, err, maxgs
    if maxgs == 0:
        return
    
    pos = data.pose.pose.position

    x = pos.x
    y = pos.y
    
    err['x'] = x_goals[curr] - pos.x
    err['y'] = y_goals[curr] - pos.y
    
    quat = data.pose.pose.orientation
    _theta = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    theta = _theta[2]
    
    err['t'] = theta_goals[curr] - _theta[2]
    if False:
        print(curr, err)

def waitandreset():
    global stopped, xstop, ystop, tstop
    stopped = True
    rospy.sleep(1.3)
    stopped = False
    xstop = ystop = False
    tstop = True

def main():
        global err, curr, xstop, ystop, tstop, flag, theta, maxgs
        curr = 0
    # Initialze Node
        # We'll leave this for you to figure out the syntax for 
        # initialising node named "controller"
        mainnode = rospy.init_node("controller")
        # Initialze Publisher and Subscriber
        # We'll leave this for you to figure out the syntax for
        # initialising publisher and subscriber of cmd_vel and odom respectively
        pub_c = rospy.Publisher("/cmd_vel",Twist, queue_size = 10)
        #pub_o = rospy.Publisher("/odom",String)
        sub_c = rospy.Subscriber("/odom", Odometry, geterror)
        rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)
        #sub_o = rospy.Subscriber("/odom",String)
        # Declare a Twist message

        # Initialise the required variables to 0
        # <This is explained below>
        
        # For maintaining control loop rate.
        rate = rospy.Rate(100)

        # Initialise variables that may be needed for the control loop
        # For ex: x_d, y_d, theta_d (in **meters** and **radians**) for defining desired goal-pose.
        # and also Kp values for the P Controller

        while(maxgs==0):
            pass
        rospy.sleep(1)
        # Control Loop goes here
        while not rospy.is_shutdown():
            # Find error (in x, y and theta) in global frame
            # the /odom topic is giving pose of the robot in global frame
            # the desired pose is declared above and defined by you in global frame
            # therefore calculate error in global frame
            

            # (Calculate error in boy_goals frame)
            # But for Controller outputs robot velocity in robot_boy_goals frame, 
                # i.e. velocity are define is in x, y of the robot frame, 
                # Notice: the direction of z axis says the same in global and boy_goals frame
                # therefore the errors will have have to be calculated in boy_goals frame.
                # 
                # This is probably the crux of Task 1, figure this out and rest should be fine.
        
                # Finally implement a P controller 
                # to react to the error with velocities in x, y and theta.

                # Safety Check
                # make sure the velocities are within a range.
                # for now since we are in a simulator and we are not dealing with actual physical limits on the system 
                # we may get away with skipping this step. But it will be very necessary in the long run.
            vel = Twist()
            if(abs(err['x'])<aerr['x']):#stop if the error is within range
                vel.linear.x = 0
                xstop=True
                
            
            if(abs(err['y'])<aerr['y']):#same as above
                vel.linear.y = 0
                ystop=True
            
            if (xstop and ystop):
                if ( abs(err['t']) < aerr['t']):
                    vel.angular.z = 0
                    pub_c.publish(vel)
                    tstop = True
                    print("%d is done now waiting!"%curr)
                    if curr<maxgs-1:
                        curr+=1
                    waitandreset()
                else:
                    e = err['t']
                    if abs(e) > pi:
                        e = -(e - pi)
                    vel.linear.x = 0
                    vel.linear.y = 0
                    vel.angular.z = e*adamp
                    tstop = False
            
            if tstop:
                vx = err['x']*damp
                vy = err['y']*damp
                print(vx, vy)
                if abs(vx) < aerr['x']:
                    vy = sign(1, vy)
                else:
                    aa = math.atan(vy/vx)
                    vx = sign(math.cos(aa), vx)
                    vy = sign(math.sin(aa), vy)
                
                vel.linear.x = mspeed * vx * math.cos(-theta) - vy * math.sin(-theta)
                vel.linear.y = mspeed * vx * math.sin(-theta) + vy * math.cos(-theta)
                vel.angular.z = 0
                xstop = False
                ystop = False
                tstop = True

            pub_c.publish(vel)
            rate.sleep()
        rospy.sleep()
                
def task1_goals_Cb(msg):
    global x_goals, y_goals, theta_goals, maxgs
    print("IN HHERREE")

    x_goals.clear()
    y_goals.clear()
    theta_goals.clear()

    for waypoint_pose in msg.poses:
        x_goals.append(waypoint_pose.position.x)
        y_goals.append(waypoint_pose.position.y)

        orientation_q = waypoint_pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        theta_goal = euler_from_quaternion (orientation_list)[2]
        theta_goals.append(theta_goal)

    maxgs = len(x_goals)
    print("I EXIT")

if __name__ == "__main__":
        try:
                main()
        except rospy.ROSInterruptException:
                pass
