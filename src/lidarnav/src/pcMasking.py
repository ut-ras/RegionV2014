import rospy
import struct
from driving.msg import Twist #mouse
from lidarnav/image import ??
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

lidar_pub = None
mousePos = None
LENGTH = 29.2608

def lidar_cb(data):
    global lidar_pub

    rospy.loginfo(rospy.get_name() + ": I heard %s", data)

    def w(x): return int(res * x/2)
    def h(y): return int(res * (0.5-(y/2)))
    # size of pic

    # ask about this
    points = [(x,y) for x,y,_,_ in pc2.read_points(data)]

    newPoints = list()
    for point in points:
        newx = mousePos[0] + point[1]
        newy = mousePos[1] + point[0]

        #        y                             x    
        if  newx <= LENGTH and newy >= LENGTH and newx >= 0 and newy >= 0:
            newPoints.append(newx)
            newPoints.append(newy)
        # displace then rotate
        # if it is then add x and y 
    packed_PC = None
    for point in newPoints:
        if not (points + 1 > len(newPoints)):
            packed_PC += struct.pack('2f',0, newPoints[point], newPoints[point + 1] )
    lidar_pub.publish(packed_PC)

def mouse_cb(data):
    global mousePos
    mousePos = data


def main():
    global points
    global lidar_pub

    rospy.init_node('PCMask')
    lidar_pub= rospy.Publisher('/PCMask/cloud', PointCloud2)
    length  = rospy.Subscriber('/mouse/pose', Twist, mouse_cb)
    points = rospy.Subscriber('cloud', PointCloud2, lidar_cb)
    map = crop out()
    
    while not rospy.is.shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)

// call back to the mouse

if__name__ == '__main__':
    main()
