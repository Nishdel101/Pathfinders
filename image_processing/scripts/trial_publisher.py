#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

global ctr


def your_mom():
    global ctr
    ctr=0
    pub = rospy.Publisher('randomstuff', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(2) # 2hz
    while not rospy.is_shutdown():
        ctr+=1
        if ctr%10==0:
            hello_str = "hello world "
        else:
            hello_str = "fuck you "
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        your_mom()
    except rospy.ROSInterruptException:
        pass
