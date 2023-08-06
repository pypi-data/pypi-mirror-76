# coding=utf-8
# Copyright 2020 The Uncertainty Metrics Authors.
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

"""Uncertainty Metrics."""

import warnings
from uncertainty_metrics import numpy
from uncertainty_metrics import tensorflow
from uncertainty_metrics.tensorflow import *

_allowed_symbols = [
    "tensorflow",
    "numpy",
]
# By default, `import uncertainty_metrics as um` uses the TensorFlow backend's
# namespace.
for name in dir(tensorflow):
  _allowed_symbols.append(name)

try:
  from tensorflow.python.util.all_util import remove_undocumented  # pylint: disable=g-direct-tensorflow-import,g-import-not-at-top
except ImportError:
  __all__ = _allowed_symbols
  try:
    import numpy as np  # pylint: disable=g-import-not-at-top,unused-import
  except ImportError:
    warnings.warn("Neither NumPy nor TensorFlow backends are available for "
                  "Uncertainty Metrics.")
else:
  remove_undocumented(__name__, _allowed_symbols)
