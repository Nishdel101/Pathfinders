#!/usr/bin/env python3
import rospy
from tf2_msgs.msg import TFMessage

def extractor(msg):
    if msg.transforms[0].child_frame_id == "base_footprint":
        print(msg)
        pub.publish(msg)
rospy.init_node('extractor')
pub = rospy.Publisher('/base_footprint', TFMessage, queue_size=1)
rospy.Subscriber('/tf', TFMessage, extractor)
rospy.spin()
