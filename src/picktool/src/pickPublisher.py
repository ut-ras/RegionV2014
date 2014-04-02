import rospy
from std_msgs.msg import String

pub = rospy.Publisher('driving', String)
rospy.init_node('hello_node')
r = rospy.Rate(10) #10Hz
while not rospy.is_shutdown()
    pub.publish("hello world")
    r.sleep()
