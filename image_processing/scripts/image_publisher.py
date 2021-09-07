#!/usr/bin/env python3
import cv2
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image
import numpy as np
import time

#set image size
Image_WIDTH=1280
Image_HEIGHT=720#960

#rospy commands
rospy.init_node('image_raw_pub',anonymous=True)
pub=rospy.Publisher('/camera/image_raw',Image,queue_size=1)
rate=rospy.Rate(30)

#opencv commands
cam = cv2.VideoCapture(0)
#cv2.namedWindow("test")

img_counter = 0

while not rospy.is_shutdown():
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
   #cv2.imshow("test", frame)

    k = cv2.waitKey(1)
#    if k%256 == 27:
#        # ESC pressed
#        print("Escape hit, closing...")
#        break
    if True:
        # SPACE pressed
        image_temp=Image()
        image_temp.header = Header(stamp=rospy.Time.now())
        image_temp.height = Image_HEIGHT
        image_temp.width = Image_WIDTH
        image_temp.encoding = 'rgb8'
        image_temp.data = np.array(frame).tostring()
        image_temp.step = Image_WIDTH*3
        pub.publish(image_temp)
        #img_name = "opencv_frame_{}.png".format(img_counter)
        #cv2.imwrite(img_name, frame)
        #print("{} written!".format(img_name))
        img_counter += 1
        rate.sleep()

cam.release()

cv2.destroyAllWindows()
