#!/usr/bin/env python
import rospy
from std_msgs.msg import String

global temp
temp="0"


def callback(data):

    global temp
    #rospy.loginfo(rospy.get_caller_id() + " middle man %s", data.data)
    print("before",temp)
    if temp!=data.data:
        temp=data.data
        #print("maybe ill publish now")
        #print("after",temp)
        pub.publish(temp)


def intermediate():
    global pub
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("image", String, callback)
    pub = rospy.Publisher('instruction', String, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    intermediate()
