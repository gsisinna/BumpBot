#!/usr/bin/env python
import rospy
import std_msgs
from geometry_msgs.msg import Point

def callback(data):
    rospy.loginfo("I heard %s \n", data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("bumpbot/global_position", Point, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
