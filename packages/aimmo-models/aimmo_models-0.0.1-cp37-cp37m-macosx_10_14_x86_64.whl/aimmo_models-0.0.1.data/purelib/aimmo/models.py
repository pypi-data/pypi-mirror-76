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

class Model:
    """
    A wrapper around a deep learning model that generated from Pytorch and Tensorflow.
    """
    def __init__(self, model):
        self.model = model

    def deploy(self):
        """
        Deploy the deep learning model to the model management system.
        """

    def predict(self, input_data):
        """
        Predict the input data using this model and then returning the result.
        """
        result = self.model.predict(input_data)
        return result
