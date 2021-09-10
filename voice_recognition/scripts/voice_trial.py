#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech, get_model_path
import rospy
from std_msgs.msg import Int16, String
import time
from playsound import playsound


global command
global speech
model_path = get_model_path()
command = "shutdown"
global previous_state
global option
previous_state = "1"
option = 0
rospy.init_node('VoiceRecognition', anonymous=True)
rate = rospy.Rate(10)

class voice_recognition():
    wordListdict = {
        '0': 0,
        'yes': 1,
        'no': 2,
        'yeah': 1,
        'nope': 2
    }

    wordsList = ['yes', 'no', 'yeah', 'nope']  # vocabulary to be increased


    rate = rospy.Rate(10)  # 10hz
    option = 0

    def __init__(self, phrase):
        self.phrase = phrase

    def listener(self):
        global option
        global previous_state
        global command
        print("here1")
        print("selfphrase:", self.phrase)
        if self.phrase in self.wordsList:
            option = self.wordListdict[self.phrase]
            print("optionhere", option)
            if command=="ask":
                if previous_state != "2" or previous_state != "5" or previous_state != "6":
                    self.choice()
                """
                elif previous_state == "2":
                    pub.publish("next_person")
                    print("next person")
                    previous_state = "2"  # or can shutdown node here
                    option = 0
                elif previous_state == "5":
                    pub.publish("follow")
                    print("follow")
                elif previous_state == "6":
                    pub.publish("go_home")
                    print("gohome")
                """

        else:  # meant to screen out words here itself as it would be faster than sending each speech message over ros publisher(and also potentially losing speechmessages)
            print("exiting")

    def choice(self):
        print("here2")
        global previous_state
        global option
        if previous_state == "1" and option == 2:
            pub.publish(5)
            previous_state = "2"
            option = 0

        elif previous_state == "1" and option == 1:
            pub.publish(6)
            print("taking med kit")
            time.sleep(10)
            pub.publish(7)
            print("asked if further assistance needed")
            previous_state = "4"

        elif previous_state == "4" and option == 1:
            pub.publish(8)
            previous_state = "5"

        elif previous_state == "4" and option == 2:
            pub.publish(9)
            previous_state = "6"

        print(previous_state, option)
    """"
    def player(self, voice):
        print("here3", voice)

        if voice == 2:
            print('see you later , bye')
            playsound('src/Pathfinders/Voice_Recognition/2.mp3')
            # place publisher code here
        if voice == 3:
            print("please take the med kit .")
            playsound('src/Pathfinders/Voice_Recognition/3.mp3')
        if voice == 4:
            print("do you need more assistance ? i can take you to the hospital")
            playsound('src/Pathfinders/Voice_Recognition/4.mp3')
        if voice == 5:
            print("follow me")
            playsound('src/Pathfinders/Voice_Recognition/5.mp3')
            # place publisher code here
        if voice == 6:
            print("Bye, im going home now")
            playsound('src/Pathfinders/Voice_Recognition/6.mp3')
            # place publisher code here
    """

def controller(msg):
    global command
    print("here4")
    if msg.data == "ask":
        command = "ask"
    if msg.data == "shutdown":
        command ="shutdown"
        print("shutdown")


rospy.Subscriber('/voice_trigger', String, controller)
pub = rospy.Publisher('/speech', Int16, queue_size=10)  # defined as Int as it is less data to send than string
print("here5")
while not rospy.is_shutdown():
    global speech
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=8000,
        buffer_size=256,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
        lm=os.path.join(model_path, 'en-us.lm.bin'),
        dic=os.path.join(model_path, 'cmudict-en-us.dict')
    )

    # try sending speech to another function
    print("here7")
    #print('speech')
    print(speech)
    # complete code goes within if command ==run voice from this point
    if command=="ask":
        if previous_state == "1" or previous_state == "2" and option == 0:
                pub.publish(4)
                previous_state="1"
    try:
        print("here8")
        for speechPhrase in speech:

            print("here6")
            print(speechPhrase, '1')  # Debugging statment
            phrase = str(speechPhrase)
            print(phrase, '2')  # Debugging statement
            subbed_msg = voice_recognition(phrase)
            subbed_msg.listener()
            # time.sleep(3)

            if previous_state == "2":
                pub.publish(1)
                print("next person")
                previous_state = "2"  # or can shutdown node here
                option = 0
                break
            elif previous_state == "5":
                pub.publish(2)
                print("follow")
                break
            elif previous_state == "6":
                pub.publish(3)
                print("gohome")
                break
    except:
        print("no speech")

    rate.sleep()
