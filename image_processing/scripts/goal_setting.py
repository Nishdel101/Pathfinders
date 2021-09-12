#!/usr/bin/env python3
import rospy
import time
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
global rate
global pub_voice
rospy.init_node('goal_setting')
rate = rospy.Rate(0.15)
area_Faces = []
area_Body = []
centre_body = 0
centre_face = 0
message = BoundingBoxes
image_width = 1280
image_height = 960
camera_angle = 65
pixel_angle = camera_angle / image_width

distances_calibrated = {
    0: 0,
    1: 1,
    2: 1.6,
    3: 2.1,
    4: 3,
    5: 5
}

def euler_to_quaternion(roll, pitch, yaw):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]

def quaternion_to_euler_angle_vectorized1(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2 > +1.0, +1.0, t2)
    # t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2 < -1.0, -1.0, t2)
    # t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.arctan2(t3, t4)

    return Z


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
    Movement(distance_to_move)
    # pub_goal.publish(distance_message)


def Body_detect(msg):
    global body_detect_flag
    global centre_body
    body_detect_flag = 1
    area_Body.clear()
    print("Body_Detect")
    for detection in msg.bounding_boxes:
        if detection.probability > 0.5 and detection.Class == 'person':
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


def Movement(distance):
    global image_width
    global pixel_angle
    global centre_body
    global pub_goal
    global rate
    global pub_voice
    new_goal = PoseStamped()
    print('Movement is working')
    #rospy.wait_for_message('/move_base/result', MoveBaseActionResult, timeout=None)
    """

    #footprint_frame = rospy.wait_for_message('/base_footprint', TFMessage, timeout=None)
    #print(footprint_frame)
    #angle_robot = quaternion_to_euler_angle_vectorized1(footprint_frame.transforms[0].transform.rotation.w,
                                                        footprint_frame.transforms[0].transform.rotation.x,
                                                        footprint_frame.transforms[0].transform.rotation.y,
                                                        footprint_frame.transforms[0].transform.rotation.z)
    #total_angle = angle_robot
    """
    movement = centre_body - (image_width / 2)

    if abs(movement) > 80:

        print(f'move {movement} pixels')
        angle_person = math.radians(pixel_angle) * movement
        #total_angle = angle_robot - angle_person

    #print(angle_robot)
    #print(total_angle)
    x_goal = (distance - 1.2) * math.cos(angle_person)
    y_goal = (distance - 1.2) * math.sin(angle_person)
    print(f'x = {x_goal} and y = {y_goal}')
    if abs(x_goal) > 1.5 or abs(y_goal) > 1.5:
        """

        new_goal.header.frame_id = 'odom'

        new_goal.pose.position.x = footprint_frame.transforms[0].transform.translation.x + x_goal
        new_goal.pose.position.y = footprint_frame.transforms[0].transform.translation.y + y_goal
        new_goal.pose.position.z = footprint_frame.transforms[0].transform.translation.z

        new_goal.pose.orientation.x = footprint_frame.transforms[0].transform.rotation.x
        new_goal.pose.orientation.y = footprint_frame.transforms[0].transform.rotation.y
        new_goal.pose.orientation.z = footprint_frame.transforms[0].transform.rotation.z
        new_goal.pose.orientation.w = footprint_frame.transforms[0].transform.rotation.w

        pub_goal.publish(new_goal)
        #rate.sleep()
        # print(pose)
        # pub_rotation = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        # make a twist message with desired rotation angle
        # pub_rotation.publish(rotation)
        # set twist message to 0 velocity
        # rotation.angular.z = 0
        # pub_rotation.publish(rotation)
        """
        new_goal.header.frame_id = 'base_link'

        new_goal.pose.position.x = x_goal
        new_goal.pose.position.y = y_goal
        new_goal.pose.position.z = 0

        new_goal.pose.orientation.x = 0
        new_goal.pose.orientation.y = 0
        new_goal.pose.orientation.z = 0
        new_goal.pose.orientation.w = 1

        pub_goal.publish(new_goal)
        #rate.sleep()
        # print(pose)
        # pub_rotation = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        # make a twist message with desired rotation angle
        # pub_rotation.publish(rotation)
        # set twist message to 0 velocity
        # rotation.angular.z = 0
        # pub_rotation.publish(rotation)
    else:
        voice_message = String()
        voice_message.data = 'ask'
        pub_voice.publish(voice_message)


"""
def read_bounding_box(msg):
    if msg.count == 0:
        pass #rotate 36 degrees
    else:
        sub_newgoal = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
"""
def Rotation_goal():

    #footprint_frame = rospy.wait_for_message('/base_footprint', TFMessage, timeout=None)
    angle_rotation = math.radians(36)

    quat = euler_to_quaternion( 0, 0, angle_rotation)

    new_goal = PoseStamped()
    #print(total_angle)
    print(f'in goal_rotation')
    """
    new_goal.header.frame_id = 'odom'

    new_goal.pose.position.x = footprint_frame.transforms[0].transform.translation.x
    new_goal.pose.position.y = footprint_frame.transforms[0].transform.translation.y
    new_goal.pose.position.z = footprint_frame.transforms[0].transform.translation.z

    new_goal.pose.orientation.x = footprint_frame.transforms[0].transform.rotation.x + quat[0]
    new_goal.pose.orientation.y = footprint_frame.transforms[0].transform.rotation.y + quat[0]
    new_goal.pose.orientation.z = footprint_frame.transforms[0].transform.rotation.z + quat[0]
    new_goal.pose.orientation.w = footprint_frame.transforms[0].transform.rotation.w + quat[0]

    pub_goal.publish(new_goal)
    #rate.sleep()
    """
    new_goal.header.frame_id = 'base_link'

    new_goal.pose.position.x = 0
    new_goal.pose.position.y = 0
    new_goal.pose.position.z = 0

    new_goal.pose.orientation.x = quat[0]
    new_goal.pose.orientation.y = quat[1]
    new_goal.pose.orientation.z = quat[2]
    new_goal.pose.orientation.w = quat[3]

    pub_goal.publish(new_goal)

def Rotation_cmd():

    pub_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity = Twist()
    velocity.linear.x = 0
    velocity.linear.y = 0
    velocity.linear.z = 0
    velocity.angular.x = 0
    velocity.angular.y = 0
    velocity.angular.z = 0.5

    pub_cmd.publish(velocity)
    rospy.sleep(10)
    velocity.angular.z = 0
    pub_cmd.publish(velocity)




def old_goal(msg):
    print('goal received')
    if msg.status.text == 'Goal reached.':
        time.sleep(5)
        print('loop is entered')
        while rospy.wait_for_message('/darknet_ros/found_object', ObjectCount, timeout=5).count == 0:
            print('rotation happening')
            Rotation_goal()
            time.sleep(5)
            
        else:
            print('bounding box loop')
            bounding_box = rospy.wait_for_message('/darknet_ros/bounding_boxes', BoundingBoxes, timeout=None)
            Body_detect(bounding_box)


    else:
        pass



pub_goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
pub_voice = rospy.Publisher('/voice_trigger', String, queue_size=10)
sub_goal = rospy.Subscriber('/move_base/result', MoveBaseActionResult, old_goal)

rospy.spin()
