#!/usr/bin/env python3
import rospy
from move_base_msgs.msg import MoveBaseActionResult
from darknet_ros_msgs.msg import ObjectCount, BoundingBoxes
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PoseStamped
import math
import numpy as np
from tf2_msgs.msg import TFMessage

'''
/move_base/result - shows Goal reached
/darknet_ros/found_object - shows count of people detected
'''

global image_width
global camera_angle
global centre_body
global centre_face
global body_detect_flag
global face_detect_flag
global area_Faces
global area_Body
global pub_goal
global pixel_angle

area_Faces = []
area_Body = []
centre_body = 0
centre_face = 0
message = BoundingBoxes
image_width = 1280
image_height = 960
camera_angle = 65
pixel_angle = camera_angle / image_width
rospy.init_node('calculating_distance')
distances_calibrated = {
    0: 0,
    1: 1,
    2: 1.6,
    3: 2.1,
    4: 3,
    5: 5
}


def area_distance(area_max):
    '''
    still to be calibrated
    :param area_max:
    :return:
    '''
    distance_message = String()
    if area_max < 50000:  # rough approx
        distance_to_move = distances_calibrated[5]  # 5 means 5 metres away and so on

    elif area_max > 50000 and area_max < 150000:  # rough approx
        distance_to_move = distances_calibrated[4]

    elif area_max > 150000 and area_max < 250000:  # based on nish and raj experiment
        distance_to_move = distances_calibrated[3]

    elif area_max > 250000 and area_max < 600000:  # based on nish and raj experiment
        distance_to_move = distances_calibrated[2]

    elif area_max > 600000 and area_max < 920000:  # based on nish and raj experiment
        distance_to_move = distances_calibrated[1]

    elif area_max > 920000:
        distance_to_move = distances_calibrated[0]

    distance_message.data = str(distance_to_move)
    print("distance of bot from person approx", distance_to_move)
    # Movement(distance_to_move)
    # pub_goal.publish(distance_message)


def Body_detect(msg):
    global body_detect_flag
    global centre_body
    body_detect_flag = 1
    area_Body.clear()
    print("Body_Detect")
    for detection in msg.bounding_boxes:
        if detection.probability > 0.5:
            length = detection.xmax - detection.xmin
            breadth = detection.ymax - detection.ymin
            area_Body.append(length * breadth)
    print(max(area_Body))
    i_body = area_Body.index(max(area_Body))
    x_max_body = msg.bounding_boxes[i_body].xmax
    x_min_body = msg.bounding_boxes[i_body].xmin
    centre_body = (x_max_body + x_min_body) / 2
    print("Body_detect : SUCCESSFUL")
    print(f'center of body is {centre_body}')
    area_distance(max(area_Body))

sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
rospy.spin()
