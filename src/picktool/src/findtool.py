#!/usr/bin/env python2
import numpy as np
import cv2
import rospy
import math

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

#from source2
import cv

image_pub = None
wthresh_pub = None
bthresh_pub = None
bridge = CvBridge()

INF = float("inf")

def distsq(a, b):
    a = a[0]; b = b[0]

    return (b[0]-a[0])**2 + (b[1]-a[1])**2

def image_cb(data):
    global image_pub, bthresh_pub, wthresh_pub
    global bridge

    img = np.asarray(bridge.imgmsg_to_cv(data))

    frame = cv2.blur(img, (8,8))
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    wthresh = cv2.inRange(hsv, np.array((0,0,150)), np.array((255,255,255)))
    wthresh[:,:5] = 0
    wthresh[:,-5:] = 0
    wthresh[:5,:] = 0
    wthresh[-5:,:] = 0
    wthresh_pub.publish(bridge.cv_to_imgmsg(cv.fromarray(wthresh), "mono8"))
    wcnts,_ = cv2.findContours(wthresh,1,1)
    wcnts = [cnt for cnt in wcnts if cv2.contourArea(cnt) > 1000]
    wcnts = np.array([p for l in wcnts for p in l])
    wcnts = np.array([[x,y] if y > 127 else (x,127) for [[x,y]] in wcnts])

    mask = np.zeros((data.height, data.width, 1), np.uint8)
    whull = cv2.convexHull(wcnts)
    whull = np.array([[[x,y+5]] for [[x,y]] in whull])
    cv2.drawContours(mask,[whull],0,(255,255,255),-1)
    mask = cv2.bitwise_not(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    img = cv2.bitwise_or(img, mask)

    frame = cv2.blur(img, (6,6))
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    bthresh = cv2.inRange(hsv, np.array((0,0,0)), np.array((255,255,100)))

    bthresh_pub.publish(bridge.cv_to_imgmsg(cv.fromarray(bthresh), "mono8"))

    bcnts,_ = cv2.findContours(bthresh,1,2)
    bcnts = [cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
             for cnt in bcnts]


    whull = np.array([[[x,y+5]] for [[x,y]] in whull])

    minangs = []
    maxangs = []

    for cnt in bcnts:
        pts = zip([cnt[-1]] + list(cnt[:-1]),
                  list(cnt),
                  list(cnt[1:]) + [cnt[0]])

        pts = [(a,b,c) for a,b,c in pts 
               if cv2.pointPolygonTest(whull, (b[0][0], b[0][1]), False) > 0]

        dists = [(distsq(a,b), distsq(b,c), distsq(a,c))
                 for a,b,c in pts]

        angs = [math.acos((a + b - c) / (2*math.sqrt(a)*math.sqrt(b)))
                for a,b,c in dists]

        minangs.append(INF if len(angs)==0 else min(angs))


        angs = [ang for ang,(a,b,c) in zip(angs, pts)
                if cv2.pointPolygonTest(whull, (a[0][0], a[0][1]), False) > 0
                and cv2.pointPolygonTest(whull, (c[0][0], c[0][1]), False) > 0]

        maxangs.append(-INF if len(angs)==0 else max(angs))



    mbcnts = sorted(zip(bcnts, minangs, maxangs), 
                    key=lambda (c,_,__): cv2.contourArea(c),
                    reverse=True)

    if len(mbcnts) < 3:
        #rospy.logwarn('No shapes detected')
        return

    mbcnts = mbcnts[:3]


    i,(triangle,_,_) = min(enumerate(mbcnts), key=lambda (_,(c,a,__)): a)
    del mbcnts[i]
    i,(circle,_,_) = max(enumerate(mbcnts), key=lambda (_,(c,__,a)): a)
    del mbcnts[i]
    rectangle,_,_ = mbcnts[0]    

    cv2.drawContours(img,[triangle],0,(255,0,0),-1)
    cv2.drawContours(img,[rectangle],0,(0,255,0),-1)
    cv2.drawContours(img,[circle],0,(0,0,255),-1)

    image_pub.publish(bridge.cv_to_imgmsg(cv.fromarray(img), "rgb8"))

    return


def main():
    global image_pub
    global bthresh_pub, wthresh_pub
    
    rospy.init_node('findtool')

    rospy.Subscriber('image', Image, image_cb)
    image_pub = rospy.Publisher('findtool/image', Image)
    bthresh_pub = rospy.Publisher('findtool/bthresh', Image)
    wthresh_pub = rospy.Publisher('findtool/wthresh', Image)

    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)

if __name__ == "__main__":
    main()
