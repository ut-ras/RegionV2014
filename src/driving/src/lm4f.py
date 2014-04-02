#!/usr/bin/env python2

import struct
import rospy
import roslib

#roslib.load_manifest('driving')

from driving.msg import Drive

def send(c, data):
    data = data * 0.85
    data = data/2 + 0.5

    with open('/dev/lm4f', 'w') as lm4f:
        ndata = int(255*data)
        lm4f.write('%c%c' % (c,ndata))
        olddata = ndata

def mcb(data):
    send('a', data.a)
    send('b', data.b)
    send('c', data.c)
    send('d', data.d)

def scb(data):
    send('e', data.a)
    send('f', data.a)
    send('g', data.a)
    send('h', data.a)

def main():
    rospy.init_node('lm4f')

    rospy.Subscriber('driving/motors', Drive, mcb);
    rospy.Subscriber('driving/servos', Drive, scb);

    rospy.spin()

if __name__ == "__main__":
    main()
