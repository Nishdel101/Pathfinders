#!/usr/bin/env python3
import rospy
#from std_msgs.msg import String
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
centre_body = 0
centre_face = 0


def Area(length,breadth):
    return length*breadth


def Body_detect(msg):
    global body_detect_flag
    body_detect_flag=1
    area_Body.clear()
    print("Body_Detect")
    try:    
        for detection in msg.bounding_boxes:
            if detection.probability > 0.5:
                length=detection.xmax - detection.xmin
                breadth=detection.ymax- detection.ymin
                area_Body.append(Area(length,breadth))
        i_body = area_Body.index(max(area_Body))
        x_max_body=msg.bounding_boxes[i_body].xmax
        x_min_body=msg.bounding_boxes[i_body].xmin
        centre_body=(x_max_body + x_min_body)/2  
        print("Body_detect : SUCCESSFUL")
        rospy.Subscriber("instruction", FaceArrayStamped, Face_detect)
    except:
        print("Body_detect : NOBODY DETECTED")
    
def Face_detect(msg):
    print("Face_Detect")
    global face_detect_flag
    face_detect_flag=1
    area_Faces.clear()
    try:
        for detection in msg.faces:
            area_Faces.append(Area(detection.face.width,detection.face.height))
        i_face= area_Faces.index(max(area_Faces))              #assuming that person with biggest body would also show the biggest face
        centre_face= msg.faces[i_face].face.x
        print("Face_detect : SUCCESSFUL")
    except:
    	print("Face_detect : NO FACE DETECTED")
    Movement()
    
def Movement(): 
    print("Movement")
    if centre_face==0 :                                          #if no face is found it just goes with the body anyways// type of movement is different
        movement = centre_body-(image_width/2)
        if movement < 80 and movement > -80 :
            print(f'move {movement} pixels')
    
    elif centre_face >= centre_body-80 and centre_face<=centre_body+80 :           #if face is present and is attached to same body//type of movement is differnet. approach face
        movement = centre_body-(image_width/2)
        if movement < 80 and movement > -80 :
            print(f'move {movement} pixels')
            
            
    elif centre_face < centre_body-80 and centre_face > centre_body+80 :            #if face is present but is not attached to the same body and is ignored// type of movement is different
        movement = centre_body-(image_width/2)
        if movement < 80 and movement > -80 :
            print(f'move {movement} pixels')
    print("Movement : SUCCESSFUL")
    
body_detect_flag=0
face_detect_flag=0
rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)
#rospy.Subscriber('instruction', String, Face_detect)
print("FINISHED CALLBACKS")
if body_detect_flag==1 and face_detect_flag==1:
    print("ENTERING MOVEMENT")
    Movement()
    body_detect_flag=0
    face_detect_flag=0
rospy.spin()
