import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

global wordList


wordsList=['yes','no','yeah','nope']

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

    phrase=str(speechPhrase)
    for word in phrase:
        print("here")
        #insert ros node code here
