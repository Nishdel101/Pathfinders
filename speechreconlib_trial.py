# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
# recognize speech using Sphinx
with sr.Microphone() as source:
    while True:
        audio = r.listen(source)
        print( r.recognize_sphinx(audio))
