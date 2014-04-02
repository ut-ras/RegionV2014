#!/usr/bin/env python2

import rospy
import roslib

from driving.msg import Drive

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

   if m0 > 1 or m1 > 1 or m2 > 1 or m3 > 1:
     mbig = max(m0, m1, m2, m3)
     m0 = m0/mbig
     m1 = m1/mbig
     m2 = m2/mbig
     m3 = m3/mbig

   if abs(m0) < .1:
     m0 = 0  
   if abs(m1) < .1:
     m1 = 0 
   if abs(m2) < .1:
     m2 = 0 
   if abs(m3) < .1:
     m3 = 0

   pubm.publish(Drive(m0, m1, m2, m3))

def mecsub(data):
    mecanum(data.a, data.b, data.c)

def main():
    global pubm

    rospy.init_node('driving')

    pubm = rospy.Publisher('driving/motors', Drive)
    subm = rospy.Subscriber('driving/velcmd', Drive, mecsub)


    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()
