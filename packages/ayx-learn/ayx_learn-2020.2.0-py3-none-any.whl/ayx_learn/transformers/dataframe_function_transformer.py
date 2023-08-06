# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Definition of DataFrameFunctionTransformer used for applying custom functions.

TODO: this is apparently used nowhere.  Maybe remove.
"""

from sklearn.base import BaseEstimator, TransformerMixin


class DataFrameFunctionTransformer(TransformerMixin, BaseEstimator):
    """Custom Transformer class which preserves pandas object types."""

    def __init__(self, fn):  # type: ignore
        self.fn = fn

    def fit(self, x, y=None, **kwargs):  # type: ignore
        """Fit the transformer."""
        return self

    def transform(self, x, y=None, copy=None, **kwargs):  # type: ignore
        """Apply the custom transform function to the input dataframe."""
        return self.fn(x)
