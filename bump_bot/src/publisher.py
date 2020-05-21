#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def subscriber():
    rospy.init_node('publisher')
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pos = "Position: %s" % rospy.get_param(pos);
        rospy.loginfo(pos)
        pub.publish(pos)
        rate.sleep()

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass