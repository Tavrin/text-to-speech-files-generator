#! /usr/bin/env python3

"""
Speech-generator: takes text and generates speech audio from Azure's Speech API using neural voices.
"""

import sys
import os
import configparser

if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # Reference:
    #  If Python version is 3.6.5
    #               major --^
    #               minor ----^
    #               micro ------^
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])

    if major != 3 or major == 3 and minor < 6:
        print("Speech-generator requires Python 3.6+\nYou are using Python %s, which is not supported by Speech-generator" % (python_version))
        sys.exit(1)

    main_config = configparser.ConfigParser()
    main_config.read(os.path.dirname(os.path.realpath(__file__)) + '/../config/config.ini')

    from SpeechGenerator import SpeechGenerator

    speech_generator = SpeechGenerator(dict(main_config.items('OPTIONS')))
    speech_generator.generate()