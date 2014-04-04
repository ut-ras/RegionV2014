#!/usr/bin/env python2

import struct
import rospy
import roslib

from driving.msg import Command

def main():
    rospy.init_node('keys')

    pubm = rospy.Publisher('driving/lm4f', Command)

    speed = rospy.get_param('~speed', 0.7)

    while not rospy.is_shutdown():
        d = None
        i = raw_input('> ')

        if i == 'w':
            d = [speed,speed,speed,speed]
        elif i == 's':
            d = [-speed,-speed,-speed,-speed]
        elif i == 'a':
            d = [speed,-speed,speed,-speed]
        elif i == 'd':
            d = [-speed,speed,-speed,speed]
        else:
            d = [0.0,0.0,0.0,0.0]

        d = Command(['a','b','c','d'], d)
        
        pubm.publish(d)

        rospy.sleep(0.25)

if __name__ == "__main__":
    main()
