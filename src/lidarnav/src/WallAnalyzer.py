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

class WallAnalyzer:
    def __init__(self, debug, pweight, kweight, res=128, dialation=(100,2)):
        self.debug = debug
        self.pweight = pweight
        self.kweight = kweight

        self.res = res
        self.dialation = dialation
        
    
        self.height = self.res*3/4
        self.width = self.res*2

        self.prev = None
        self.prevd = None
        self.preva = None
        
        self.wall_angle = None
        self.wall_ydistance = None
        self.wall_arr = None
        self.out_img = None


    def uangle(self, a, b):
        r = -math.atan2(-a[1]*b[0] + a[0]*b[1], 
                        numpy.dot(a, b))

        if r > PI2: r = PI - r
        if r < -PI2: r = -PI - r
        
        return (PI2 - abs(r))/PI2


    def update(self, data):
        def w(x): 
            return int(self.res * (.5-x))
        def h(y): 
            return int(self.res * (1.0-y))
        def dist(l):
            return ((l[0]-l[2])**2 + (l[1]-l[3])**2)

        img = numpy.zeros((self.height,self.width,1), numpy.uint8)
        out = numpy.zeros((self.height,self.width,3), numpy.uint8)

        points = [(x,y) for x,y,_,_ in pc2.read_points(data)]

        for x,y in ((w(x),h(y)) for x,y in points):
            if x+1 < self.height and y+1 < self.width and x >= 0 and y >= 0:
                img[x,y] = 255

        cvimg = cv.fromarray(img)

        if self.prev:
            def weight(l):
                return (self.kweight * self.uangle((l[2]-l[0], l[3]-l[1]), 
                                         (self.prev[2]-self.prev[0], self.prev[3]-self.prev[1])) +
                        self.pweight * sum(1 if p else 0 for p in cv.InitLineIterator(
                                      cvimg, (l[0], l[1]), (l[2], l[3]))))
        else:
            def weight(l):
                return sum(1 if p else 0 for p in cv.InitLineIterator(
                           cvimg, (l[0], l[1]), (l[2], l[3])))


        lines = cv2.HoughLinesP(img, 1, PI/180, 5)

        mline = None


        if len(lines > 0):
            lines = lines[0] 

            lines = [(0, (-x*vy)/vx + y,
                      self.width-1, ((self.width-x)*vy)/vx + y) for vx,vy,x,y in
                        ((x1-x0, y1-y0, x0, y0) for x0,y0,x1,y1 in 
                            lines) if vx != 0]

            if len(lines) > 0:
                mline = max(lines, key=weight)


        self.prev = mline

        # mline now contains our target line
        a = numpy.array([float(mline[0]), float(mline[1])])
        n = numpy.array([float(mline[2]-mline[0]), float(mline[3]-mline[1])])
        n = n/numpy.linalg.norm(n)
        p = (self.width/2, self.height)

        # distance
        dist = numpy.subtract(a,p)
        dist = numpy.subtract(dist, numpy.dot(dist, n) * n)
        self.prevd = numpy.linalg.norm(dist)

        # orientation
        self.preva = math.atan2(n[1], n[0])

        # pixel array
        #M = cv2.getRotationMatrix2D((self.width/2,self.height/2), self.preva*180/math.pi, 1)
        #img = cv2.warpAffine(img, M, (self.width,self.height))    

        kernel = numpy.ones(self.dialation, numpy.uint8)
        img = cv2.dilate(img, kernel)
        lineItr = cv.InitLineIterator(cv.fromarray(img), (0, self.height/2), (self.width, self.height/2))

        # publish data
        self.wall_angle = self.preva
        self.wall_ydistance = self.prevd
        self.wall_arr = [True if p else False for p in lineItr]
        
        if self.debug:
            line = ""
            for i in range(len(self.wall_arr)/3):
                p = self.wall_arr[i*3]
                line += 'X' if p else ' '
            print line
            
            out = cv2.cvtColor(img, cv.CV_GRAY2BGR)
            cv2.line(out, (mline[0], mline[1]), (mline[2], mline[3]), (255,0,0), 1)
            
            self.out_img = cv.fromarray(out)


