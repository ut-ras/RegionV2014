#!/usr/bin/env python2

import rospy
import roslib


def main():
    rospy.init_node('driving')

    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()
