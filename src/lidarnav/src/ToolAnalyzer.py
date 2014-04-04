#!/usr/bin/env python2

import math
import numpy
import cv2
import cv

import rospy
import roslib
from roslib import message

import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from lidarnav.msg import WallState

PI = math.pi
PI2 = math.pi/2

class ToolAnalyzer:
    def __init__(self, debug, res=64, dialation=(7,7)):
        self.debug = debug

        self.res = res
        self.dialation = dialation
    
        self.height = self.res
        self.width = self.res

        self.out_img = None


    def uangle(self, a, b):
        r = -math.atan2(-a[1]*b[0] + a[0]*b[1], 
                        numpy.dot(a, b))

        if r > PI2: r = PI - r
        if r < -PI2: r = -PI - r
        
        return (PI2 - abs(r))/PI2


    def update(self, data):
        def w(x): 
            return int(self.res * (.5-x) *2)
        def h(y): 
            return int(self.res * (.25-y) *2)
        def dist(l):
            return ((l[0]-l[2])**2 + (l[1]-l[3])**2)

        img = numpy.zeros((self.height,self.width,1), numpy.uint8)
        out = numpy.zeros((self.height,self.width,3), numpy.uint8)

        points = [(x,y) for x,y,_,_ in pc2.read_points(data)]

        for x,y in ((w(x),h(y)) for x,y in points):
            if x+1 < self.height and y+1 < self.width and x >= 0 and y >= 0:
                img[x,y] = 255

        out = cv2.cvtColor(img, cv.CV_GRAY2BGR)       
 
        img = cv2.blur(img,(3,3)) 
        img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)[1]
        out[:,:,0] = img[:,:]
        
        kernel = numpy.ones(self.dialation, numpy.uint8)
        img = cv2.dilate(img, kernel)
        out[:,:,1] = img[:,:]
        
        contours, hieracy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, (0, 0, 255), 1)
       
        
 
        if self.debug:
            self.out_img = cv.fromarray(out)


