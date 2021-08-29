#!/usr/bin/env python3
import rospy
from darknet_ros_msgs.msg import BoundingBoxes
from opencv_apps.msg import FaceArrayStamped

rospy.init_node('moving_image')

image_width = 1280
image_height = 720

message = BoundingBoxes


global centre_body
global centre_face
global body_detect_flag
global face_detect_flag
global area_Faces
global area_Body
area_Faces=[]
area_Body=[]
centre_body = []
centre_face = []


def Area(length,breadth):
    return length*breadth


def Body_detect(msg):
    global body_detect_flag
    body_detect_flag=1
    for detection in msg.bounding_boxes:
        if detection.probability > 0.5:
            length=detection.xmax - detection.xmin
            breadth=detection.ymax- detection.ymin
            area_Body.append(Area(length,breadth))
    i_body = area_Body.index(max(area_Body))
    x_max_body=msg.bounding_boxes[i_body].xmax
    x_min_body=msg.bounding_boxes[i_body].xmin
    centre_body=(x_max_body + x_min_body)/2  
    
def Face_detect(msg):
    global face_detect_flag
    face_detect_flag=1
    for detection in msg.faces:
        area_Faces.append(Area(detection.width,detection.height))
    i_face= area_Faces.index(max(area_Faces))              #assuming that person with biggest body would also show the biggest face
    centre_face= msg.faces[i_face].face.x
    
def Movement(): 
    if centre_face >= centre_body+80 and centre_face<=centre_body+80 :
        movement = center_body-(image_width/2)
        if movement > 80 or movement < -80 :
            print(f'move {movement} pixels')

rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
rospy.Subscriber('/face_detection/faces', FaceArrayStamped, Face_detect)
if body_detect_flag==1 and face_detect_flag==1:
    Movement()
    body_detect_flag=0
    face_detect_flag=0
rospy.spin()

