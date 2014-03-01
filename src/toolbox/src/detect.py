#!/usr/bin/env python2

import rospy
from /rgb/image_raw
import roslib

#weird stuff
import numpy as np
import cv2


def main():
    rospy.init_node('detect')

    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()

img = cv2.imread('shapes.png')
gray = cv2.imread('shapes.png',0)

ret,thresh = cv2.threshold(gray,177,255,1)

contours,h = cv2.findContours)thresh,1,2)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==3:
        print "triangle"
        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        print "square"
        cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) > 15:
        print "circle"
        cv2.drawContours(img,[cnt],0(0.255.255),-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
