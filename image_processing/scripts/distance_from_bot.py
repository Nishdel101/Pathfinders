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


distances_calibrated = {
	0:0,
	1:1,
	2:2,
	3:3,
	4:4,
	5:5
}

def area_distance(area_max):
    
    if area_max<50000 :		#rough approx
        distance_to_move=distances_calibrated[5]	#5 means 5 metres away and so on  
        
    elif area_max>50000 and area_max<150000 :		#rough approx
        distance_to_move=distances_calibrated[4] 
    
    elif area_max>150000 and area_max<250000 :	#based on nish and raj experiment
        distance_to_move=distances_calibrated[3]    
    
    elif area_max>250000 and area_max<600000 :	#based on nish and raj experiment
        distance_to_move=distances_calibrated[2] 
        
    elif area_max>600000 and area_max<920000 :		#based on nish and raj experiment
        distance_to_move=distances_calibrated[1] 
        
    elif area_max>920000 :
        distance_to_move=distances_calibrated[0] 
        
    print("distance of bot from person approx", distance_to_move)
    
    
    
    
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
                area_Body.append(length*breadth)
        print(max(area_Body))
        i_body = area_Body.index(max(area_Body))
        x_max_body=msg.bounding_boxes[i_body].xmax
        x_min_body=msg.bounding_boxes[i_body].xmin
        centre_body=(x_max_body + x_min_body)/2  
        print("Body_detect : SUCCESSFUL")
        area_distance(max(area_Body))
        
    except:
        print("Body_detect : NOBODY DETECTED")
    

rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, Body_detect)

rospy.spin()
