#!/usr/bin/env python3

"""
logic-
code scans speech, converts it to a string, and checks if the string contains one of the words we require
it then maps this word accordingly to a number specified in the word dictionary(as it takes less data ad hence higher probability of success i think , to send an integer via ros pub.)
this integer is passed to the pub class and sent to the bot to tell the bot if for example it has to look for another person or whatever.
"""
"""
next idea is to have the bot saz something and if answered , the bot reads and depending on the answer the bot changes the hmiphase variable which will again cause the bot to
say something else and then again change the him variable. epending on the kez instruction , the bot will then send data via the Publisher
"""

import os
from pocketsphinx import LiveSpeech, get_model_path, Pocketsphinx

import rospy
from std_msgs.msg import Int16
import time

model_path = get_model_path()

global wordsList
global assistanceFlag
global command
global personReachedFlag

wordsList=['yes','no','yeah','nope']        #vocabulary to be increased


wordListdict = {
    'yes':1,
    'no':2,
    'yeah':3,
    'nope':4
}


def voicePublisher():
    pub = rospy.Publisher('/speech', Int16, queue_size=10) #defined as Int as it is less data to send than string
    pub_play = rospy.Publisher('/sound_play',Int16, queue_size=10)
    rospy.init_node('VoiceRecognition', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg=Int16()
    hmiPhase=Int16()
    config = {             
    		'hmm': os.path.join(model_path, 'en-us'),
            	'lm':os.path.join(model_path, 'en-us.lm.bin'),
            	'dict':os.path.join(model_path, 'cmudict-en-us.dict')
     }
     
    ps=Pocketsphinx(**config)
     
     
    while not rospy.is_shutdown():

        speech=ps.decode(
     
            buffer_size=256,
            no_search=False,
            full_utt=False,

        )

        command =0
        assistanceFlag=0
        personReachedFlag=0
        hmiPhase.data=1
        pub_play.publish(hmiPhase)
        
	#print(speechPhrase,'1')    #Debugging statment
        phrase=str(speech)
	print(phrase,'2')          #Debugging statement
	


        msg.data=command       #Debugging statement
        rospy.loginfo(msg.data)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    voicePublisher()
