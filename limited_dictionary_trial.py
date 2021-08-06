#! Python 3.9.6
"""
logic-
code scans speech, converts it to a string, and checks if the string contains one of the words we require
it then maps this word accordingly to a number specified in the word dictionary(as it takes less data ad hence higher probability of success i think , to send an integer via ros pub.)
this integer is passed to the pub class and sent to the bot to tell the bot if for example it has to look for another person or whatever.

'BEFORE CODING FURTHER'
line 60 is debug and line 61 is the actual ros pub method call so when trying to publish , comment and uncomment the apt lines


"""

import os
from pocketsphinx import LiveSpeech, get_model_path
"""
import rospy
from std_mdsgs.msg import Int16
"""
model_path = get_model_path()
global wordList
wordsList=['yes','no','yeah','nope']        #vocabulary to be increased

wordListdict = {
    'yes':1,
    'no':2,
    'yeah':3,
    'nope':4
}

"""
def voicePublisher(pubInt):
    pub = rospy.Publisher('Speech', Int16, queue_size=10) #defined as Int as it is less data to send than string
    rospy.init_node('VoiceRecognition', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        publishedInteger = pubInt % rospy.get_time()
        rospy.loginfo(PublishedInteger)
        pub.publish(PublishedInteger)
        rate.sleep()
"""

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
        print(wordListdict[phrase])          #Debugging statement
        #voicePublisher(wordListdict[phrase])
