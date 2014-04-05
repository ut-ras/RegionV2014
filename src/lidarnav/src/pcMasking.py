#!/usr/bin/env python2
import rospy
import roslib
import roslib.message
import struct
from driving.msg import Twist #mouse
#from lidarnav/image import ??
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

lidar_pub = None
mousePos = (0,0)
LENGTH = 2.4

def lidar_cb(data):
    global lidar_pub

    rospy.loginfo(rospy.get_name() + ": I heard %s", data)

    def w(x): return int(res * x/2)
    def h(y): return int(res * (0.5-(y/2)))
    # size of pic

    # ask about this
    oldPoints = [(x,y) for x,y,_,_ in pc2.read_points(data)]
    newPoints = list()
    for point in oldPoints:
            newx = mousePos[1] + point[0]
            newy = mousePos[0] + point[1]
            #        y                             x    
            if  newx <= LENGTH and newy >= LENGTH and newx >= 0 and newy >= 0:
                newPoints.append([newx,newy])
            # displace then rotate
            # if it is then add x and y 
    packed_PC = ""
    for point in newPoints:
        packed_PC += struct.pack('2f', point[0], point[1])
    lidar_pub.publish(PointCloud2(data=packed_PC))

def mouse_cb(data):
    global mousePos
    mousePos = (data.x,data.y)


def main():
    global points
    global lidar_pub

    rospy.init_node('PCMask')
    lidar_pub= rospy.Publisher('/PCMask/cloud', PointCloud2)
    length  = rospy.Subscriber('/mouse/pose', Twist, mouse_cb)
    points = rospy.Subscriber('/cloud', PointCloud2, lidar_cb)
    
    while not (rospy.is_shutdown()):
        rospy.loginfo('hello')
        rospy.sleep(1)

# call back to the mouse

if __name__ == '__main__':
    main()
