#!/usr/bin/env python2
import rospy, cv, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
import numpy as np

bridge = CvBridge()
cv_image = None

class ColorTracker:
    #def __init__(self):
        #cv2.namedWindow("Color Tracker")
    def run(self):
        #while(1):
            global cv_image
            if cv_image is None:
                return
            frame = cv2.blur(np.asarray(cv_image),(3,3))
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(hsv,np.array((60, 190, 145)), np.array((100, 255, 255)))
            thresh2 = thresh.copy()
            #thresh2 = cv2.inRange(hsv,np.array((0, 0, 0)), np.array((255, 255, 40)))
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            print 'x: ', cx
            cv2.circle(frame,(cx,cy),5,255,-1)
            cv2.imshow('frame',frame)
            cv2.imshow('thresh',thresh2)
            if cx < 270:
                print 'MISALIGNED MOVE LEFT'
            elif cx >= 270 and cx <= 280:
                print 'CORRECT PUT IN TOOL'
            elif cx > 280:
                print 'MISALIGNED MOVE RIGHT'
            else:
                print 'ERROR'
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
def callback(data):
    global cv_image
#    rospy.loginfo(rospy.get_name() + ": I heard %s", data)
    cv_image = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")

def  listener():
    rospy.init_node('node_name')
    rospy.Subscriber("image",Image, callback)
    color_tracker = ColorTracker()

    while not rospy.is_shutdown():
        color_tracker.run()
       #rospy.spin()

if __name__ == '__main__':
    listener()
