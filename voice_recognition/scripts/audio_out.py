#!/usr/bin/env python3


import os
from pocketsphinx import LiveSpeech, get_model_path
import rospy
from std_msgs.msg import Int16, String
import time
from playsound import playsound
from geometry_msgs.msg import Twist, PoseStamped

global pub_goal
global new_goal
new_goal = PoseStamped()
new_goal.header.frame_id = 'map'

new_goal.pose.position.x = 0
new_goal.pose.position.y = 0
new_goal.pose.position.z = 0

new_goal.pose.orientation.x = 0
new_goal.pose.orientation.y = 0
new_goal.pose.orientation.z = 0
new_goal.pose.orientation.w = 1

def callback(voice):
    print("here3", voice)
    global new_goal

    if voice.data == 4:
        print("im here to help. Did you ask for this medkit")
        playsound('src/Pathfinders/voice_Recognition/voice_files/1.mp3')
    if voice.data == 5:
        print('see you later , bye')
        playsound('src/Pathfinders/voice_Recognition/voice_files/2.mp3')
        pub_goal.publish(new_goal)
        # place publisher code here
    if voice.data == 6:
        print("please take the med kit .")
        playsound('src/Pathfinders/voice_Recognition/voice_files/3.mp3')
    if voice.data == 7:
        print("do you need more assistance ? i can take you to the hospital")
        playsound('src/Pathfinders/voice_Recognition/voice_files/4.mp3')
    if voice.data == 8:
        print("follow me")
        playsound('src/Pathfinders/voice_Recognition/voice_files/5.mp3')
        pub_goal.publish(new_goal)
        # place publisher code here
    if voice.data == 9:
        print("Bye, im going home now")
        playsound('src/Pathfinders/voice_Recognition/voice_files/6.mp3')
        pub_goal.publish(new_goal)
        # place publisher code herccx4789*613--**6541111122233--++..00e


rospy.init_node('sound_player')
pub_goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
rospy.Subscriber('/speech', Int16, callback)

rospy.spin()
