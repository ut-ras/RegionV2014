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

    def getPoints(self, data):
        def w(x): 
            return int(self.res * (.5-x) *2)
        def h(y): 
            return int(self.res * (.25-y) *2)

        img = numpy.zeros((self.height,self.width,1), numpy.uint8)

        if self.debug:
            out = numpy.zeros((self.height,self.width,3), numpy.uint8)

        points = [(x,y) for x,y,_,_ in pc2.read_points(data)]

        for x,y in ((w(x),h(y)) for x,y in points):
            if x+1 < self.height and y+1 < self.width and x >= 0 and y >= 0:
                img[x,y] = 255

        if self.debug:
            out = cv2.cvtColor(img, cv.CV_GRAY2BGR)       
 
        img = cv2.blur(img,(3,3)) 
        img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)[1]
        
        if self.debug:
            out[:,:,0] = img[:,:]
        
        kernel = numpy.ones(self.dialation, numpy.uint8)
        img = cv2.dilate(img, kernel)

        if self.debug:
            out[:,:,1] = img[:,:]
        
        contours, hieracy = cv2.findContours(
            img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=lambda x:-cv2.arcLength(x, True))[0:3]

        # sum each contour
        centers = []
        for i in range(len(contours)):
            center = [0,0]
            for p in contours[i]:
                center[0] += p[0][0]
                center[1] += p[0][1]
            center[0] /= len(contours[i]) 
            center[1] /= len(contours[i]) 
            centers.append(center)
 
        if self.debug:
            cv2.drawContours(out, contours, -1, (0, 0, 255), 1)
            for c in centers:
                cv2.circle(out, (c[0], c[1]), 10, (255,0,0))
                self.out_img = out

        return centers

    def getPosOfTool(self, index, cloud):
        points = sorted(self.getPoints(cloud), key=lambda p:p[0])
        
        if len(points) != 3:
            rospy.logerr("tool location detection: detecting "+len(points)+" contours instead of 3")
            return False

        p = points[index]

        if self.debug:
            cv2.circle(self.out_img, (p[0], p[1]), 10, (255,255,0))
            self.out_img = cv.fromarray(self.out_img)
        
        return p


