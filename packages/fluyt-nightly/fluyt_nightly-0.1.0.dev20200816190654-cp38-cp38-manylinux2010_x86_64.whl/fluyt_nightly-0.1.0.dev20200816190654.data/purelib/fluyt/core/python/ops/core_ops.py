# Copyright 2020 Yong Tang. All Rights Reserved.
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
# ==============================================================================
"""fluyt"""

import tensorflow as tf


class Layer(tf.keras.layers.Layer):
    def __init__(self, transform):
        super().__init__()
        self._transform = transform
        self._w = transform._param[0]
        self._b = transform._param[1]

    def __call__(self, input):
        return self._transform(input)
