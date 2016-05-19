#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Authors: Konstantinos Panayiotou, Manos Tsardoulias
# contact: klpanagi@gmail.com, etsardou@iti.gr


import os
import timeit
import rospkg
from os import path

__path__ = os.path.dirname(os.path.realpath(__file__))

from RappCloud import RappPlatformService
from RappCloud.CloudMsgs import SpeechRecognitionGoogle


class RappInterfaceTest:

  def __init__(self):
    rospack = rospkg.RosPack()
    pkgDir = rospack.get_path('rapp_testing_tools')
    audioFile = path.join(pkgDir, 'test_data',
        'speech_detection_samples', 'recording_sentence2.ogg')

    self.msg = SpeechRecognitionGoogle(
        language='en',
        audio_source='nao_ogg',
        audiofile=audioFile)

    self.svc = RappPlatformService(self.msg)

    self.valid_words_found = ['check', 'my', 'mail']


  def execute(self):
    start_time = timeit.default_timer()
    response = self.svc.call()
    end_time = timeit.default_timer()
    self.elapsed_time = end_time - start_time
    return self.validate(response)


  def validate(self, response):
    error = response.error
    if error != "":
      return [error, self.elapsed_time]

    words_found = response.words
    alt_words_found = response.alternatives
    if self.valid_words_found == words_found or self.valid_words_found in alt_words_found:
        return [True, self.elapsed_time]
    else:
        return ["Unexpected result : " + str(response), self.elapsed_time]

