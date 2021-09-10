#!/usr/bin/env python3


import os
from pocketsphinx import LiveSpeech, get_model_path
import rospy
from std_msgs.msg import Int16, String
import time
from playsound import playsound


def callback(voice):
    print("here3", voice)


    if voice.data == 4:
        print("im here to help. Did you ask for this medkit")
        playsound('src/Pathfinders/Voice_Recognition/1.mp3')
    if voice.data == 5:
        print('see you later , bye')
        playsound('src/Pathfinders/Voice_Recognition/2.mp3')
        # place publisher code here
    if voice.data == 6:
        print("please take the med kit .")
        playsound('src/Pathfinders/Voice_Recognition/3.mp3')
    if voice.data == 7:
        print("do you need more assistance ? i can take you to the hospital")
        playsound('src/Pathfinders/Voice_Recognition/4.mp3')
    if voice.data == 8:
        print("follow me")
        playsound('src/Pathfinders/Voice_Recognition/5.mp3')
        # place publisher code here
    if voice.data == 9:
        print("Bye, im going home now")
        playsound('src/Pathfinders/Voice_Recognition/6.mp3')
        # place publisher code herccx4789*613--**6541111122233--++..00e


rospy.init_node('sound_player')
rospy.Subscriber('/speech', Int16, callback)

rospy.spin()
