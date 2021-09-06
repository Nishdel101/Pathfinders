#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech, get_model_path
import rospy
from std_msgs.msg import Int16, String
import time
from playsound import playsound


"""

logic-

subcriber callback-
    callback goes to main method in voice recon class
    
voice recon class
            enters main method
    



"""
class voice_recognition()

    previous_state="0"
    next_state="0"
    phrase=0
    wordsList=['yes','no','yeah','nope']        #vocabulary to be increased
    pub = rospy.Publisher('/speech', Int16, queue_size=10) #defined as Int as it is less data to send than string
    rospy.init_node('VoiceRecognition', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    wordListdict = {
        'yes':1,
        'no':2,
        'yeah':1,
        'nope':2
    }
    def __init__(self):

    def controller(self,msg):

        if msg.data=="run_voice":
            self.listener(command)
        if msg.data=="shutdown":
            print("shutdown")

    def listener(self):

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
        for speechPhrase in speech:
            #print(speechPhrase,'1')    #Debugging statment
            phrase=str(speechPhrase)
            #print(phrase,'2')          #Debugging statement
            if phrase in wordsList: #meant to screen out words here itself as it would be faster than sending each speech message over ros publisher(and also potentially losing speechmessages)
                self.option=wordListdict[phrase]
        if self.previous_state!="2" || self.previous_state!="5" || self.previous_state!="6":
            self.choice()
        elif self.previous_state=="2":
            pub.publish("next_person")
            self.previous_state="0" #or can shutdown node here
            self.option="0"
        elif self.previous_state=="5":
            pub.publish("follow")
        elif self.previous_state=="6":
            pub.publish("go_home")


    def choice(self):

        if self.previous_state =="0" and self.option=="0"
            self.player(1)
            self.previous_state="1"

        if self.previous_state =="1" and self.option=="2"
            self.player(2)
            self.previous_state="2"

        if self.previous_state =="1" and self.option=="1"
            self.player(3)
            time.sleep(10)
            self.player(4)
            self.previous_state="4"

        if self.previous_state =="4" and self.option=="1"
            self.player(5)
            self.previous_state="5"

        if self.previous_state =="4" and self.option=="2"
            self.player(6)
            self.previous_state="6"

    def player(self,voice):
        if voice== 1:
            print("im here to help. Did you ask for this medkit")
            playsound('src/Pathfinders/Voice_Recognition/1.mp3')
        if voice== 2:
            print('see you later , bye')
            playsound('src/Pathfinders/Voice_Recognition/2.mp3')
            #place publisher code here
        if voice== 3:
            print("please take the med kit .")
            playsound('src/Pathfinders/Voice_Recognition/3.mp3')
        if voice== 4:
            print("do you need more assistance ? i can take you to the hospital")
            playsound('src/Pathfinders/Voice_Recognition/4.mp3')
        if voice== 5:
            print("follow me")
            playsound('src/Pathfinders/Voice_Recognition/5.mp3')
            #place publisher code here
        if voice== 6:
            print("Bye, im going home now")
            playsound('src/Pathfinders/Voice_Recognition/6.mp3')
            #place publisher code here



subbed_msg=voice_recognition()
rospy.Subscriber('/voice_commands', String, subbed_msg.controller(msg))
