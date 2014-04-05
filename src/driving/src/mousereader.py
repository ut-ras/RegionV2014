#!/usr/bin/env python2

import rospy
import roslib
import struct

from driving.srv import SetTwist, SetTwistResponse
from driving.msg import Twist

pub = None
mouse = None

scale = None
xsum = 0
ysum = 0

def reset(data):
    global pub
    global scale
    global xsum, ysum

    xsum, ysum = data.x, data.y
    pub.publish(Twist(x=data.x, y=data.y, a=0))
    return SetTwistResponse()


def getMouseEvent():
    global mouse

    buf = mouse.read(3)
    x,y = struct.unpack( "bb", buf[1:] )

    return x,y
    # return stuffs


def main():
    global mouse
    global pub
    global scale
    global xsum, ysum

    rospy.init_node('mousereader')
    mouse = open('/dev/input/mice', 'rb')
    
    rospy.Service('mouse/reset', SetTwist, reset)
    pub = rospy.Publisher('mouse/pose', Twist)

    scale = float(rospy.get_param('~scale', 0.001*(1/34.463)))

    rospy.loginfo('Initialized mousereading')

    while not rospy.is_shutdown():
        x,y = getMouseEvent()
        xsum += x
        ysum += y

        pub.publish(Twist(x=scale*xsum, y=scale*ysum, a=0))

    mouse.close()

if __name__ == "__main__":
    main()
