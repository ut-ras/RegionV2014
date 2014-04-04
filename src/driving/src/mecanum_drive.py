#!/usr/bin/env python2

import rospy
import roslib

from driving.msg import Command
from driving.msg import Twist

pubm = None

def mecanum(vx, vy, r):
   global pubm

   # x translation
   m0 = -vx
   m1 = vx
   m2 = vx
   m3 = -vx

   # y translation
   m0 += vy
   m1 += vy
   m2 += vy
   m3 += vy

   # rotation
   m0 += r
   m1 += -r
   m2 += r
   m3 += -r

   ms = [m0,m1,m2,m3]

   if any(abs(m) > 1 for m in ms):
     mbig = max(abs(m) for m in ms)
     ms = [m/mbig for m in ms]

   ms = [m if abs(m) >= 0.1 else 0 for m in ms]

   pubm.publish(Command(['a','b','c','d'], ms))

def mecsub(data):
    mecanum(data.x, data.y, data.a)

def main():
    global pubm

    rospy.init_node('driving')

    pubm = rospy.Publisher('driving/lm4f', Command)
    subm = rospy.Subscriber('driving/velcmd', Twist, mecsub)


    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()
