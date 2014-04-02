import rospy
from sensor_msgs.msg import Image

def callback (data):
    rospy.loginfo(rospy.get_name() + "I heard %s", data)

def listener():
    rospy.init_node('node_name')
    rospy.Subscriber("/usb_cam/image_raw",Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
