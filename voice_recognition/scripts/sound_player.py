#!/usr/bin/env python3

import os
import rospy
from playsound import playsound
from std_msgs.msg import Int16



def callback(msg):
    if msg.data == 1:
        print("im here to help. Did you ask for this medkit")
        playsound('~/ROS/Pathfinders/Voice_Recognition/1.mp3')
    if msg.data == 2:
        print('see you later , bye')
        playsound('~/ROS/Pathfinders/Voice_Recognition/2.mp3')
    if msg.data == 3:
          
        playsound('~/ROS/Pathfinders/Voice_Recognition/3.mp3')
    if msg.data == 4:

        playsound('~/ROS/Pathfinders/Voice_Recognition/4.mp3')
    if msg.data == 5:

        playsound('~/ROS/Pathfinders/Voice_Recognition/5.mp3')
    if msg.data == 6:

        playsound('~/ROS/Pathfinders/Voice_Recognition/6.mp3')

rospy.init_node('sound_player')
rospy.Subscriber('/sound_play', Int16, callback)
rospy.spin()
