#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from opencv_apps.msg import FaceArrayStamped

global temp
temp="0"


def callback(data):
    #print("checkingtype",type(data))
    global temp
    #rospy.loginfo(rospy.get_caller_id() + " middle man %s", data.data)
    #print("before",temp)
    if temp!=data.faces:
        #print("data.faces",data.faces)
        temp=data.faces
        #print("maybe ill publish now")
        #print("after",temp)
        pub.publish(data)  #weird fix but temp changes to a list because of data.faces and has to be converted back because of the publish function


def intermediate():
    global pub
    print("running")
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("face_detection/faces", FaceArrayStamped, callback)
    pub = rospy.Publisher('instruction', FaceArrayStamped, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    intermediate()
