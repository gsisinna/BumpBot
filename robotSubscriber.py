#!/usr/bin/env python
import rospy
import std_msgs
from geometry_msgs.msg import Point
from bump_bot.srv import *

gridSize = rospy.get_param("/gridSize")

def set_direction_client(x, y):    
    try:
        rospy.loginfo("Service invoked!")
        resp = set_direction(x, y)
        resp.x = x - 2
        resp.y = y - 2
        return resp.x, resp.y
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

def callback(data):
    rospy.loginfo("(x,y): %d, %d \n", data.x, data.y)
    if data.x == gridSize-1 and data.y == gridSize-1:
        rospy.wait_for_service('set_direction')
        req = rospy.ServiceProxy('/set_direction', set_direction)
        rospy.loginfo("Changing direction, I'm stuck!")
        
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("bumpbot/global_position", Point, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
