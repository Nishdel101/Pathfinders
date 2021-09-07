#!/usr/bin/env python3
import rospy
from move_base_msgs.msg import MoveBaseActionResult
from darknet_ros_msgs.msg import ObjectCount, BoundingBoxes
from std_msgs.msg import String
from geometry_msgs.msg import Twist

'''
/move_base/result - shows Goal reached
/darknet_ros/found_object - shows count of people detected
'''

image_width = 1280
image_height = 720

message = BoundingBoxes

global centre_body
global centre_face
global body_detect_flag
global face_detect_flag
global area_Faces
global area_Body
area_Faces = []
area_Body = []
centre_body = 0
centre_face = 0
global pub_goal

distances_calibrated = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5
}


def area_distance(area_max):
    global pub_goal
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
    pub_goal.publish(distance_message)


def Body_detect(msg):
    global body_detect_flag
    global centre_body
    body_detect_flag = 1
    area_Body.clear()
    print("Body_Detect")
    try:
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
        Movement()
        print("Body_detect : SUCCESSFUL")
        area_distance(max(area_Body))

    except:
        print("Body_detect : NOBODY DETECTED")


def Movement():
    global centre_body
    movement = centre_body - (image_width / 2)
    if movement < -80 and movement > 80:
        print(f'move {movement} pixels')
        pub_rotation = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        #make a twist message with desired rotation angle
        pub_rotation.publish(twist_message)
        #give time delay
        #set twist message to 0 velocity
        pub_rotation.publish(twist_message)


"""
def read_bounding_box(msg):
    if msg.count == 0:
        pass #rotate 36 degrees
    else:
        sub_newgoal = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
"""


def old_goal(msg):
    if msg.status.text == 'Goal reached.':
        while rospy.wait_for_message('/darknet_ros/found_object', ObjectCount, timeout=None).count == 0:
            continue  # Rotation
        else:
            bounding_box = rospy.wait_for_message('/darknet_ros/bounding_boxes', BoundingBoxes, timeout=None)
            Body_detect(bounding_box)


    else:
        pass


rospy.init_node('goal_setting')
pub_goal = rospy.Publisher('/movement', String, queue_size=1)
sub_goal = rospy.Subscriber('/move_base/result', MoveBaseActionResult, old_goal)

rospy.spin()
