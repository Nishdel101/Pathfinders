#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def voiceSubscriber():

    rospy.init_node('VoiceRecognitionSub', anonymous=True)

    rospy.Subscriber("Speech", Int16, callback)

    rospy.spin()

if __name__ == '__main__':
    voiceSubscriber()
