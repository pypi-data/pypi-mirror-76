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
"""Definition of the DropNaRowsTransformer.

# TODO: should probably do / offer re-indexing.

"""
from typing import Any

from ayx_learn.typing import ArrayLike

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class DropNaRowsTransformer(TransformerMixin, BaseEstimator):
    """Transformer for rows with missing values in a specified column."""

    def __init__(self, colname: str, inplace: bool = False) -> None:
        """Construct transformer.

        Parameters
        ----------
        colname : str
            Name of column to search for missing values.

        inplace : bool (default: False)
            whether .transform is applied in-place.

        """
        self.colname = colname
        self.inplace = bool(inplace)

    def fit(
        self, x: ArrayLike, y: ArrayLike = None, **_: Any
    ) -> "DropNaRowsTransformer":
        """Fit transformer.  No-op in this case.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Fitting dependent data

        y : pandas.Series or array-like, shape = (n_observations), optional
            Fitting target observations

        **_ :
            Additional arguments to mop up

        Returns
        -------
        self

        """
        return self

    def transform(self, df):  # type: ignore
        """Transform data, dropping rows where .colname is missing.

        Parameters
        ----------
        df : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        Returns
        -------
        pandas.DataFrame with rows where .colname is missing dropped

        """
        inplace = self.inplace

        assert isinstance(df, pd.DataFrame)
        assert self.colname in list(df)

        result = df.dropna(subset=[self.colname], inplace=inplace)
        if not inplace:
            df = result

        return df
