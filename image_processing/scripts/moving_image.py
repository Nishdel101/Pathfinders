#!/usr/bin/env python3
import rospy
from darknet_ros_msgs.msg import BoundingBoxes

rospy.init_node('moving_image')

image_width = 1280
image_height = 720

message = BoundingBoxes


global centre_body
global centre_face
global body_detect_flag
global face_detect_flag
centre_body = []
centre_face = []


def Area(length,breadth):
    return length*breadth


def Body_detect(msg):
    body_detect_flag=1
    for detection in msg.bounding_boxes:
        if detection.probability > 0.5:
            length=detection.xmax - detection.xmin
            breadth=detection.ymax- detection.ymin
            area_Body.append(Area(length,breadth))
    i_body = area_Body.index(max(area))
    x_max_body=msg.bounding_boxes[i].xmax
    x_min_body=msg.bounding_boxes[i].xmin
    centre_body=(x_max_body + x_min_body)/2  
    
def Face_detect(msg):
    face_detect_flag=1
    for detection in msg.faces:
        area_Face.append(Area(detection.width,detection.height))
    i_face= area_faces.index(max(area))              #assuming that person with biggest body would also show the biggest face
    centre_face= msg.faces[i_face].face.x)
    
def Movement(): 
    if centre_face >= centre_body+80 and centre_face<=centre_body+80 :
        movement = center_body-(image_width/2)
        if movement > 80 or movement < -80 :
            print(f'move {movement} pixels')

rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
rospy.Subscriber('/open_CV/bounding_boxes', Faces, Face_detect)
if body_detect_flag==1 and face_detect_flag==1:
    Movement()
    body_detect_flag=0
    face_detect_flag=0
rospy.spin()

