#!/usr/bin/env python3
import rospy
from move_base_msgs.msg import MoveBaseActionResult
from darknet_ros_msgs.msg import ObjectCount, BoundingBoxes
from std_msgs.msg import String
from geometry_msgs.msg import Twist
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
image_height = 720
camera_angle = 65
pixel_angle = camera_angle/image_width

distances_calibrated = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5
}
def quaternion_to_euler_angle_vectorized1(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return Z

def area_distance(area_max):


    '''
    still to be calibrated
    :param area_max:
    :return:
    '''
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
    Movement()
    pub_goal.publish(distance_message)


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


def Movement():
    global image_width
    global pixel_angle
    global centre_body
    print ('Movement is working')
    movement = centre_body - (image_width / 2)
    if movement > abs(80):

        pose = TFMessage()
        print(f'move {movement} pixels')
        angle_person = math.radians(pixel_angle)*movement
        footprint_frame = rospy.wait_for_message('/base_footprint', TFMessage, timeout=None)
        angle_robot = quaternion_to_euler_angle_vectorized1(footprint_frame.transforms[0].transform.rotation.w, footprint_frame.transforms[0].transform.rotation.x, footprint_frame.transforms[0].transform.rotation.y, footprint_frame.transforms[0].transform.rotation.z)
        total_angle = angle_person + angle_robot
        print(angle_robot)
        print(total_angle)


        #print(pose)
        #pub_rotation = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        #make a twist message with desired rotation angle
        #pub_rotation.publish(rotation)
        #set twist message to 0 velocity
        #rotation.angular.z = 0
        #pub_rotation.publish(rotation)


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
