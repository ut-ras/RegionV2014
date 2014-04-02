#!/usr/bin/env python2

import struct
import rospy
import roslib

from driving.msg import Drive

def main():
    rospy.init_node('keys')

    pubm = rospy.Publisher('driving/motors', Drive)
    pubs = rospy.Publisher('driving/servos', Drive)

    speed = rospy.get_param('~speed', 0.7)

    while not rospy.is_shutdown():
        d = None
        i = raw_input('> ')

        if i == 'w':
            d = Drive(speed,speed,speed,speed)
        elif i == 's':
            d = Drive(-speed,-speed,-speed,-speed)
        else:
            d = Drive(0.0,0.0,0.0,0.0)

        pubm.publish(d)
        pubs.publish(d)

        rospy.sleep(0.25)

if __name__ == "__main__":
    main()
