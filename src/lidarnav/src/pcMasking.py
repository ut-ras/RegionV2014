import rospy
from driving.msg import Twist #mouse
from lidarnav/image import ??
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

points = None



def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s", data)

def listener():
    rospy.init_node('node_name')
    rospy.Subscriber("/usb_cam/image_raw", Image, callback)
    rospy.spin()



def main():
    global points

    global mouse_pos # updates mouse position

    rospy.init_node('pcMask')


    rospy.Subscriber('/mouse/pose', Twist, callback)
    

    rospy.Subscriber('cloud', PointCloud2, lidar_cb)

    
    while not rospy.is.shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)

// call back to the mouse

if__name__ == '__main__':
    main()
