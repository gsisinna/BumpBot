#!/usr/bin/env python
import rospy
import random
import std_msgs
from geometry_msgs.msg import Point
import numpy

class robot:
    def __init__ (self, position):
        self.position = position

    def get_position(self):
        return self.position

    def move_x(self, unit):
        self.position[0] += unit

    def move_y(self, unit):
        self.position[1] += unit

    def move_rand(self):
        move = random.choice([self.move_x, self.move_x, self.move_y, self.move_y])
        units = random.choice([1,1,1,-1]) 
        move(units)

    def check_walls(self, gridSize):
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > gridSize-1:
            self.position[0] = gridSize-1
        elif self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > gridSize-1:
            self.position[1] = gridSize-1
            

if __name__ == '__main__':
    myRobot = robot([0,0])
    
    rospy.init_node('publisher')
    pub = rospy.Publisher('bumpbot/global_position', Point, queue_size=10)
    rate = rospy.Rate(1)

    #gridSize = rospy.get_param("gridSize")
    gridSize = 10
    
    while not rospy.is_shutdown():
        myRobot.move_rand()
        myRobot.check_walls(gridSize)

        x_coord = myRobot.position[0]
        y_coord = myRobot.position[1]

        p = Point()
        p.x = x_coord
        p.y = y_coord
        p.z = 0

        #p = "Position [x,y]: " + str(x_coord) + " " + str(y_coord)
        rospy.loginfo(p)
        pub.publish(p)
        rate.sleep()
        
        if x_coord > gridSize-1:
            myRobot.move_x(-1)
        elif y_coord > gridSize-1:
            myRobot.move_y(-1);
        elif x_coord < 0:
            myRobot.move_x(1)
        elif y_coord < 0:
            myRobot.move_y(1)

        matrix = numpy.zeros((gridSize,gridSize), numpy.int8)
        matrix[x_coord, y_coord] = 1
        print(matrix)
