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
"""Python module for AIMMO specific deep learning model deployment"""
import getpass
import os
import sys
import torch
import requests

from pkg_resources import get_distribution
from model_archiver.model_packaging import generate_model_archive

__version__ = get_distribution("aimmo-models").version

class Model:
    """
    A wrapper around a deep learning model that generated from Pytorch and Tensorflow.
    """
    def __init__(self, model):
        # Support only Torch model for now
        assert model.__class__.mro()[1] is torch.nn.modules.module.Module
        self.model = model

    def deploy(self, version, task, model_file, **kwargs):
        """
        Deploy the deep learning model to the model management system.
        """
        # 모델 이름이 지정되지 않으면 모델 클래스 이름을 모델 이름으로 설정한다.
        model_name = self.model.__class__.__name__
        if 'model_name' in kwargs.keys():
            model_name = kwargs['model_name']

        state_dict_file = '/tmp/{}.pth'.format(model_name)

        # 모델 아카이브 파일 생성할 경로 설정
        export_path = '/tmp'
        if 'export_path' in kwargs.keys():
            export_path = kwargs['export_path']

        cmd_params = {
            '--model-name'      : model_name,
            '--serialized-file' : state_dict_file,
            '--model-file'      : model_file,
            '--handler'         : task,
            '--version'         : version,
            '--export-path'     : export_path,
        }

        if 'extra_files' in kwargs.keys():
            cmd_params['--extra-files'] = kwargs['extra_files']

        # 모델 파일 아카이빙
        self._archive(cmd_params)

        # 모델 아카이브 파일 업로드
        url = os.environ['UPLOADER_URL'] + '/upload_model'
        user_id = input('Torch Serve ID: ')
        user_password = getpass.getpass('Torch Serve Password: ')
        files = {'file': open(os.path.join(export_path, model_name + '.mar'), 'rb')}
        res = requests.post(url, files=files, auth=(user_id, user_password))
        return res

    def predict(self, input_data):
        """
        Predict the input data using this model and then returning the result.
        """
        assert isinstance(input_data, torch.Tensor)
        result = self.model(input_data)
        return result

    def _archive(self, cmd_params):
        """
        Archive this model as .mar file.
        """
        # Save the state dict as serialized file (.pth)
        torch.save(self.model.state_dict(), cmd_params['--serialized-file'])

        # HACK: torch-model-archiver 커맨드라인 파라메터 설정
        for param, value in cmd_params.items():
            sys.argv.append(param)
            sys.argv.append(value)

        # 동일한 아카이브 파일이 존재하면 덮어씀
        sys.argv.append('-f')

        # torch model 아카이빙 (torch-model-archiver 커맨드 실행과 동일)
        generate_model_archive()
