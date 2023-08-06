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

import abc

import tensorflow as tf


class Param:
    def __init__(self, value):
        self._transform = None
        self._reference = tf.Variable(value, trainable=True)

    @property
    def reference(self):
        return self._reference

    def value(self):
        return (
            self._reference.value()
            if self._transform is None
            else self._transform(self._reference)
        )


class Prototype(abc.ABC):
    @abc.abstractproperty
    def param(self):
        raise NotImplementedError("Prototype.param")

    @abc.abstractmethod
    def __call__(self, input):
        raise NotImplementedError("Prototype.__call__")


class Layer(tf.keras.layers.Layer):
    def __init__(self, transform):
        super().__init__()
        self._transform = transform
        if isinstance(transform, Prototype):
            for i, e in enumerate(transform.param):
                e = e.reference if isinstance(e, Param) else e
                setattr(self, f"_param_{i}", e)

    def __call__(self, input):
        return self._transform(input)
