#!/usr/bin/env python2
import rospy, cv, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
import numpy as np

from fireman.msg import ShapeList
from fireman.srv import Shape, ShapeResponse

bridge = CvBridge()
ipub = None

detected = False
value = 0


def colortrack(data):
    global detected, value
    global ipub

    cv_image = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")

    frame = cv2.blur(np.asarray(cv_image),(3,3))
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((0, 0, 0)), np.array((255, 255, 40)))
    thresh2 = thresh.copy()
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

    rospy.loginfo('x: %d', cx)

    cv2.circle(frame,(cx,cy),5,255,-1)

    ipub.publish(bridge.cv_to_imgmsg(cv.fromarray(frame), "bgr8"))
    #cv2.imshow('frame',frame)
    #cv2.imshow('thresh',thresh2)

    if cx <= 195:
        rospy.loginfo('Left Side, RECTANGLE')
        value = 1
    elif cx > 195 and cx <= 355:
        rospy.loginfo('Middle Side, CIRCLE')
        value = 2
    elif cx > 355:
        rospy.loginfo('Right Side, TRIANGLE')
        value = 3
    else:
        rospy.logwarn('Error, NOTHING')
        value = 0

    detected = True

    #if cv2.waitKey(0) == 27:
    #    cv2.destroyAllWindows()


def detect(data):
    global detected, value

    sub = rospy.Subscriber('image', Image, colortrack)
    rospy.loginfo('Waiting for image')
    detected = False

    while not detected:
        rospy.sleep(0.1)

    sub.unregister()
    return ShapeList([value])


#def listener():
#    rospy.init_node('node_name')
#    rospy.Subscriber("image",Image, callback)
#    color_tracker = ColorTracker()
#
#    while not rospy.is_shutdown():
#        color_tracker.run()
#       #rospy.spin()

def main():
    global ipub

    rospy.init_node('detect')

    ipub = rospy.Publisher('fireman/image', Image)
    rospy.Service('fireman/detect', Shape, detect)
    rospy.spin()

if __name__ == '__main__':
    main()
