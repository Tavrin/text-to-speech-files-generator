import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import os
import json
from dotenv import load_dotenv
import math

load_dotenv()

class SpeechGenerator():
    __language = 'fr-FR'
    __name = 'fr-FR-HenriNeural'
    __service_region = 'francecentral'
    __api_key = None
    __speech_synthesis_output_format = 'Riff24Khz16BitMonoPcm'
    sdk_config = {}
    __json_path = '../output/items.json'
    __output_type = 'speaker'
    __csv_file = '../speech.csv'
    __file_name_format = 'enumerate'
    __file_path = '../output'

    def __init__(self, config):
        self.setProperties(config)

    def setProperties(self, config):
        if ('language' in config):
            self.__language = config['language']

        if ('name' in config):
            self.__name = config['name']

        if ('region' in config):
            self.__service_region = config['region']

        if ('output_format' in config):
            self.__speech_synthesis_output_format = config['output_format']

        if ('output_type' in config):
            self.__output_type = config['output_type']

        if ('csv_file' in config):
            self.__csv_file = os.getcwd() + config['csv_file']

        if ('json_path' in config):
            self.__json_path = os.getcwd() + config['json_path']

        if ('file_path' in config):
            self.__file_path = os.getcwd() + config['file_path']

        if ('file_name_format' in config):
            self.__file_name_format = config['file_name_format']

        if (os.getenv('API_KEY') is None):
            raise ValueError('No API KEY added to .env file')

        self.__api_key = os.getenv('API_KEY')

    def generate(self):
        self.initializeSdkConfig()
        items = self.setJson()

        data = pd.read_csv(self.__csv_file, encoding='utf8')

        for index, column in enumerate(data.speech):
            print(column)

            number = index + 1

            if True == isinstance(data.description[index], str) or False == math.isnan(float(data.description[index])):
                print(data.description[index])
                description = data.description[index]
            else:
                description = column

            if (self.__file_name_format == 'enumerate'):
                file_path = self.__file_path + '/sound' + str(number) + '.wav'
            else:
                print(column.replace(" ", "_"))
                file_path = self.__file_path + '/' + column.replace(" ", "_") + '.wav'

            item = {
                "name": "sound" + str(number),
                "file": file_path,
                "description": description
            }

            items["items"].append(item)

            text = column

            if (self.__output_type == 'file'):
                self.sdk_config['audio_config'] = speechsdk.audio.AudioOutputConfig(filename=file_path)
            else:
                self.sdk_config['audio_config'] = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

            self.sdk_config['speech_synthesizer'] = speechsdk.SpeechSynthesizer(speech_config = self.sdk_config['speech_config'], audio_config = self.sdk_config['audio_config'])
            result = self.sdk_config['speech_synthesizer'].speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized to speaker for text [{}]".format(text))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        print("Error details: {}".format(cancellation_details.error_details))

        with open(self.__json_path, 'w') as outfile:
            json.dump(items, outfile, indent=4, ensure_ascii=False)


    def initializeSdkConfig(self):
        self.sdk_config['speech_config'] = speechsdk.SpeechConfig(subscription = self.__api_key, region = self.__service_region)
        self.sdk_config['speech_config'].set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat[self.__speech_synthesis_output_format])
        self.sdk_config['speech_config'].speech_synthesis_language = self.__language
        self.sdk_config['speech_config'].speech_synthesis_voice_name = self.__name

    def setJson(self):
        with open(self.__json_path, 'w') as outfile:
            items = {
                "items": []
            }
            json.dump(items, outfile)

        with open(self.__json_path, 'r') as infile:
            items = json.load(infile)
            items["items"] = []

            return items