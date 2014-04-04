#!/usr/bin/env python2

import struct
import rospy
import roslib
import serial

from driving.msg import Command


lm4f = None

def send(c, data):
    global lm4f

    data = data/2 + 0.5
    ndata = int(255*data)
    lm4f.write('%c%c\n' % (c,ndata))
    lm4f.read(2)

def cmd(data):
    for c,v in zip(data.cmds, data.vals):
        send(c, v)

def main():
    global lm4f

    rospy.init_node('lm4f')
    lm4f = serial.Serial(port='/dev/lm4f',
                         baudrate=115200,
                         timeout=1)

    rospy.Subscriber('driving/lm4f', Command, cmd);

    rospy.spin()
    lm4f.close()


if __name__ == "__main__":
    main()
