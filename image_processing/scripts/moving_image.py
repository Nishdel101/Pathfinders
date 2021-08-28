#!/usr/bin/env python3

import rospy
from darknet_ros_msgs.msg import BoundingBoxes

rospy.init_node('moving_image')

image_width = 1280
image_height = 720

message = BoundingBoxes


def Area(msg):
    length = msg.xmax - msg.xmin
    breadth = msg.ymax - msg.ymin
    return length*breadth

def rotation(msg):
    area = []
    center = []
    
    for detection in msg.bounding_boxes:
        if detection.probability > 0.5:
            area.append(Area(detection))
    i = area.index(max(area))
    center = (msg.bounding_boxes[i].xmax + msg.bounding_boxes[i].xmin)/2
    movement = center-(image_width/2)
    if movement > 50 or movement < -50 :
        print(f'move {movement} pixels')


rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, rotation)

rospy.spin()
