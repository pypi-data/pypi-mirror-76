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
"""Definition of the ColumnTypeTransformer for applying data typing to a dataframe."""
from typing import Any, Optional

from ayx_learn.utils.constants import ColumnTypes
from ayx_learn.utils.typing import typing_conversions
from ayx_learn.utils.validate import validate_col_type

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class ColumnTypeTransformer(TransformerMixin, BaseEstimator):
    """Transformer used to apply typing coercions to dataframe."""

    def __init__(
        self,
        coltype: str = ColumnTypes.NUMERIC,
        colname: Optional[str] = None,
        inplace: bool = False,
        **kwargs: Any
    ):
        """Construct transformer.

        Parameters
        ----------
        coltype : str  (default: 'NUMERIC')
            Member of ayx_learn.utils.constants.ColumnTypes

        colname : str, optional
            If provided, only transform by applying transformer to specified column.
            Else, apply to entire dataframe.

        inplace : bool (default: False)
            whether .transform is applied inplace

        """
        self.coltype = coltype
        self.colname = colname
        self._inplace = bool(inplace)

    @property
    def coltype(self) -> str:
        """Getter for column type of this transformer."""
        return self.__coltype

    @coltype.setter
    def coltype(self, value: str) -> None:
        """Setter for column type of this transformer."""
        validate_col_type(value)
        self.__coltype = value

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data, coercing column(s) to self.coltype.

        Parameters
        ----------
        X : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        Returns
        -------
        pandas.DataFrame with converted columns, shape = (n_feature, n_observations)

        """
        columns_to_transform = X.columns
        if self.colname is not None:
            columns_to_transform = [self.colname]
        inplace = self._inplace
        if not inplace:
            X = X.copy()
        # Apply transformation columnwise
        for column in columns_to_transform:
            X.loc[:, column] = typing_conversions[self.coltype](  # type: ignore
                X[column]
            )
        return X

    def fit(
        self, X: Optional[pd.DataFrame], y: Optional[pd.Series] = None, **kwargs: Any
    ) -> "ColumnTypeTransformer":
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
