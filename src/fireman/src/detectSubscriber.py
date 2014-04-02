#!/usr/bin/env python2
import rospy, cv, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
import numpy as np

bridge = CvBridge()
cv_image = None
color_tracker_window = "Color Tracker"

class ColorTracker:
    def __init__(self):
        cv.NamedWindow(color_tracker_window,1)
    def run(self):
        while True:
            global cv_image
            if cv_image is None:
                return
            img = cv_image
            cv.Smooth(img,img, cv.CV_BLUR, 3);
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3);
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)
            thresholded_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
            cv.InRangeS(hsv_img, (0, 0, 0), (255, 255, 80), thresholded_img)
            mat = cv.GetMat(thresholded_img)
            moments = cv.Moments(mat, 0)
            area = cv.GetCentralMoment(moments, 0, 0)
            if(area>100000):
                x = cv.GetSpatialMoment(moments, 1, 0)/area
                y = cv.GetSpatialMoment(moments, 0, 1)/area
                print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area)
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
                cv.Circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
                cv.Add(img, overlay, img)
                cv.Merge(thresholded_img, None, None, None, img)
            cv.ShowImage(color_tracker_window, img)
            #cv.WaitKey(0)
            if cv.WaitKey(10) == 27:
                break
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
