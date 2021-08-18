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
from playsound import playsound
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

def commandRecognition(hmiPhase):
    if hmiPhase==1:
        print("im here to help. Did you ask for this medkit")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')
    elif hmiPhase==2:
        print("see you later , bye")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')
    elif hmiPhase==3:
        print("please take the med kit .")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')

    elif hmiPhase==4:
        print("do you need more assistance ? i can take you to the hospital")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')

    elif hmiPhase==5:
        print("follow me")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')

    elif hmiPhase==6:
        print("Bye, im going home now")
        playsound('/home/mascor/Downloads/496088_dastudiospr_finger-snap.mp3')


def voicePublisher():
    pub = rospy.Publisher('Speech', Int16, queue_size=10) #defined as Int as it is less data to send than string
    rospy.init_node('VoiceRecognition', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg=Int16()
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
        hmiPhase=1
        command =0
        assistanceFlag=0
        personReachedFlag=0
        commandRecognition(1)
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
                        commandRecognition(3)
                        personReachedFlag=1
                        command=1
                        time.sleep(10)
                        commandRecognition(4)
                        assistanceFlag=1
                    else :

                        commandRecognition(5)
                        command=3

                elif option==2 or option==4:
                    print("said no")
                    if personReachedFlag==0:
                        commandRecognition(2)
                    else :
                        commandRecognition(6)
                        command=2



        msg.data=command         #Debugging statement
        rospy.loginfo(msg.data)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    voicePublisher()
