#!/usr/bin/env python2

import rospy
import roslib
from cv_bridge import CvBridge
import detectSubscriber

bridge = CvBridge()
cv_image = bridge.imgmsg_to_cv(image_message, desired_encoding="passthrough")

def main():
    rospy.init_node('detect')

    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()
