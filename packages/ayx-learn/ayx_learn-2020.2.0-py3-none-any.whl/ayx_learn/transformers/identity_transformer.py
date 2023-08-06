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
"""Definition of the IdentityTransformer."""
from typing import Any, Optional, TypeVar

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


T = TypeVar("T", bound="IdentityTransformer")


class IdentityTransformer(TransformerMixin, BaseEstimator):
    """Transformer that does nothing.

    Acts similarly to sklearn's usage of 'passthrough'.
    """

    def __init__(self, **kwargs: Any):
        """Construct transformer.

        Parameters
        ----------
        **kwargs
            Arguments to mop up.

        """
        pass

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Do not transform data; return as inputted.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to not transform.

        Returns
        -------
        X
            data passed in as X

        """
        return X

    def inverse_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Inverse of transform; also does nothing.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to not transform.

        Returns
        -------
        X
            data passed in as X

        """
        return X

    def fit(
        self: T, X: pd.DataFrame, y: Optional[pd.Series] = None, **kwargs: Any
    ) -> T:
        """Fit transformer.  No-op in this case.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Fitting dependent data

        y : pandas.Series or array-like, shape = (n_observations), optional
            Fitting target observations

        **kwargs :
            Additional arguments to mop up

        Returns
        -------
        self

        """
        return self
