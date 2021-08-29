#!/usr/bin/envs python3

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
from pocketsphinx import LiveSpeech, get_model_path

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
    while not rospy.is_shutdown():

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

        command =0
        assistanceFlag=0
        personReachedFlag=0
        hmiPhase.data=1
        pub_play.publish(hmiPhase)
        for speechPhrase in speech:
            #print(speechPhrase,'1')    #Debugging statment
            phrase=str(speechPhrase)
            #print(phrase,'2')          #Debugging statement
            if phrase in wordsList: #meant to screen out words here itself as it would be faster than sending each speech message over ros publisher(and also potentially losing speechmessages)
                option=wordListdict[phrase]
                print(option)
                if option==1 or option==3:
                    print("said yes")
                    if assistanceFlag==0:
                        hmiPhase.data=3
                        pub_play.publish(hmiPhase)
                        personReachedFlag=1
                        command=1
                        time.sleep(10)
                        hmiPhase.data=4
                        pub_play.publish(hmiPhase)
                        assistanceFlag=1
                    else :

                        hmiPhase.data=5
                        pub_play.publish(hmiPhase)
                        command=3

                elif option==2 or option==4:
                    print("said no")
                    if personReachedFlag==0:
                        hmiPhase.data=2
                        pub_play.publish(hmiPhase)
                    else :
                        hmiPhase.data=6
                        pub_play.publish(hmiPhase)
                        command=2



        msg.data=command       #Debugging statement
        rospy.loginfo(msg.data)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    voicePublisher()
