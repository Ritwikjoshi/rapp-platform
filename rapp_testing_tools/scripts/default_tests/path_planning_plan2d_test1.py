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

from RappCloud import RappPlatformAPI

class RappInterfaceTest:

  def __init__(self):
    rospack = rospkg.RosPack()
    pkgDir = rospack.get_path('rapp_testing_tools')
    
    testDatapath = path.join(pkgDir, 'test_data', 'path_planning')

    self.poseStart = {
        'header':{
            'seq': 0, 'stamp':{'sec': 0, 'nsecs': 0}, 'frame_id': ''
        },
        'pose': {
            'position': {'x': 1, 'y': 1, 'z': 0},
            'orientation': {'x': 0, 'y': 0, 'z': 0, 'w': 0}
        }
    }

    self.poseGoal = {
        'header':{
            'seq': 0, 'stamp':{'sec': 0, 'nsecs': 0}, 'frame_id': ''
        },
        'pose': {
            'position': {'x': 5.3, 'y': 4, 'z': 0},
            'orientation': {'x': 0, 'y': 0, 'z': 20, 'w': 0}
        }
    }

    self.yamlFile = path.join(testDatapath, '523_m_obstacle_2.yaml')
    self.pngFile = path.join(testDatapath, '523_m_obstacle_2.png')
    self.map_name='523_m_obstacle_2'

    self.ch = RappPlatformAPI()

  def execute(self):
    start_time = timeit.default_timer()
    resp = self.ch.pathPlanningUploadMap(self.map_name, self.pngFile, self.yamlFile)
    # If error occured while uploading map return error
    if resp['error'] != '':
       return self.validate(resp)

    resp = self.ch.pathPlanningPlan2D(self.map_name, 'NAO', self.poseStart,\
            self.poseGoal)

    end_time = timeit.default_timer()
    self.elapsed_time = end_time - start_time
    return self.validate(resp)

  def validate(self, response):
    error = response['error']
    if error != "":
      return [error, self.elapsed_time]
    else:
      return [True, self.elapsed_time]
