# Copyright 2020 AIMMO CO., LTD. All Rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python module for AIMMO specific deep learning model management server"""
import json
from os.path import exists
from os.path import join
from pathlib import Path
import requests

class Server:
    """
    A wrapper around a deep learning model that generated from Pytorch and Tensorflow.
    """
    def __init__(self, url=None):
        # 모델 업로더 백엔드 URL 설정
        self.url = url
        if self.url is None:
            config_file_name = join(str(Path.home()), '.aimmo_models', 'config.json')
            assert exists(config_file_name)
            config = ''
            with open(config_file_name, 'r') as config_file:
                config = json.load(config_file)
            self.url = config['url']
            assert self.url is not None

    def model_list(self):
        """
        List-up the deployed models
        """
        url = self.url + '/models/'
        res = requests.get(url, auth=('aimmo', 'datalab'))

        return res.text

    def model_info(self, model_name, version="v1.0"):
        end_point = self.url + '/models/' + model_name
        res = requests.get(end_point, auth=('aimmo', 'datalab'))
        if res.status_code != 200:
            print("Failed to get the model information."
                  "Check the 'model_name' or server alive state")
            return None

        return res.text

    def upload_model(self, archive_file_path):
        """
        Upload the archived model file (.mar)
        """
        end_point = self.url + '/upload_model'
        files = {'file': open(archive_file_path, 'rb')}
        res = requests.post(end_point, files=files, auth=('aimmo', 'datalab'))

        return res
