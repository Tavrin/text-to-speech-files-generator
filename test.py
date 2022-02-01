import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import os
import json
from dotenv import load_dotenv
import math

load_dotenv()

speech_key, service_region = os.getenv('API_KEY'), "francecentral"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])

speech_config.speech_synthesis_language = "fr-FR"  # For example, "de-DE"
speech_config.speech_synthesis_voice_name = "fr-FR-HenriNeural"

#set the path to the json file
json_file = "./sounds/items.json"

 # create the json file if it doesn't exist
if not os.path.exists(json_file):
    items = {
        "sound": {
            "items": []
        }
    }
    with open(json_file, 'w') as outfile:
        json.dump(items, outfile)


# if the json file exists and has data, empty it
if os.path.exists(json_file):
    with open(json_file, 'r') as infile:
        items = json.load(infile)
        items["sound"]["items"] = []

data = pd.read_csv("example/speech.csv", encoding='utf8')

for index, column in enumerate(data.speech):
    print(column)

    number = index + 1

    if True == isinstance(data.description[index], str) or False == math.isnan(float(data.description[index])):
        print(data.description[index])
        description = data.description[index]
    else:
        description = column

    item = {
        "selector": {
            "name": "sound" + str(number) + "Selector",
            "file": "public/assets/items/sound/selectors/sound" + str(number) + ".png"
        },
        "item": {
            "name": "sound" + str(number),
            "file": "public/assets/items/sound/sound" + str(number) + ".wav",
            "description": description
        }
    }

    items["sound"]["items"].append(item)

    text = column
    audio_config = speechsdk.audio.AudioOutputConfig(filename="./sounds/sound" + str(number) + '.wav')
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))


with open(json_file, 'w') as outfile:
    json.dump(items, outfile, indent=4, ensure_ascii=False)