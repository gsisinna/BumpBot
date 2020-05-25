#!/usr/bin/env python
import rospy
import random
import std_msgs
from geometry_msgs.msg import Point
from bump_bot.srv import set_direction, set_directionResponse
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
        self.units = random.choice([1, 1, -1, -1])
        move(self.units)

    def check_walls(self, gridSize):
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > gridSize-1:
            self.position[0] = gridSize-1
        elif self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > gridSize-1:
            self.position[1] = gridSize-1

    def handle_set_direction(self, req):
        rospy.loginfo("Changing direction, I'm stuck!")
        
        self.position[0] = req.x
        self.position[1] = req.y
        
        if req.x and req.y == gridSize-1:
            self.units = random.choice([-1, -1, -1, 1])
        else:
            self.units = random.choice([1, 1, 1, -1])
        
        return set_directionResponse(req.x, req.y)
    
    def set_direction_server(self):
        s = rospy.Service('set_direction', set_direction, self.handle_set_direction)
        print "Ready to change direction."
            

if __name__ == '__main__':
    myRobot = robot([0,0])
    
    rospy.init_node('publisher')
    pub = rospy.Publisher('bumpbot/global_position', Point, queue_size=10)
    rate = rospy.Rate(10)

    myRobot.set_direction_server()

    rospy.set_param('gridSize', 10)
    gridSize = rospy.get_param("/gridSize")
    #matrix = numpy.zeros((gridSize,gridSize), numpy.int)

    while not rospy.is_shutdown():
        myRobot.move_rand()
        myRobot.check_walls(gridSize)

        x_coord = myRobot.position[0]
        y_coord = myRobot.position[1]

        p = Point()
        p.x = x_coord
        p.y = y_coord
        p.z = 0

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

        # Solo per debug veloce, eliminare print() alla fine e sostituire su /rosout
        
        #matrix[x_coord, y_coord] = 1
        #print(matrix)
        #matrix[x_coord, y_coord] = 0

