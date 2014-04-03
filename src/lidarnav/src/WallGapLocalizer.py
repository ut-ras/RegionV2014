#!/usr/bin/env python
import rospy
from lidarnav.msg import WallState

class WallGapLocalizer:
    def __init__(self, debug, gapSize=50, startingLocation=0):
        self.debug = debug
        self.gapSize = gapSize
        self.inFrontOfWave = False
        self.prevCenter = None
        self.location = startingLocation
        self.canMoveForward = False

    def update(self, arr):
        start = len(arr)/2

        prevInFrontOfWave = self.inFrontOfWave
        self.inFrontOfWave = arr[start]

        # go left
        leftIndex = start
        leftLen = 0
        while leftIndex > start - self.gapSize:
            if arr[leftIndex] == self.inFrontOfWave:
                leftLen += 1
            else:
                break
            leftIndex -= 1

        # go right
        rightIndex = start
        rightLen = 0
        while rightIndex < start + self.gapSize:
            if arr[rightIndex] == self.inFrontOfWave:
                rightLen += 1
            else:
                break
            rightIndex += 1


        # see if the gap is big enough
        self.canMoveForward = not self.inFrontOfWave and leftLen >= self.gapSize/2 and rightLen >= self.gapSize/2
        
        # move our location by how much the center of the gap or wave has moved since last time
        center = (leftIndex + rightIndex)/2
        if self.prevCenter == None:
            self.prevCenter = center
        
        if self.inFrontOfWave == prevInFrontOfWave:
            self.location += (center - self.prevCenter)
        
        # if in the center of something, correct the location to reflect that
        if abs(leftLen - rightLen) < 2:
            self.location = round(self.location/float(self.gapSize/2)) * self.gapSize/2
        
        self.prevCenter = center
      
        if self.debug: 
            print self.canMoveForward, self.location, leftLen, rightLen


