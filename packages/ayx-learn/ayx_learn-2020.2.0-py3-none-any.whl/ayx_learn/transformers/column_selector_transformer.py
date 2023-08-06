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
"""Column select and column drop data frame transformer.

# TODO: deprecate support for regex in favor of column name strings

"""
import re
from typing import Any, List, Optional, TypeVar

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

T = TypeVar("T", bound="ColumnSelectorTransformer")


class ColumnSelectorTransformer(TransformerMixin, BaseEstimator):
    """Transformer used to select/deselect a set of columns based on regex.

    Column Selector/Deselector: Takes a list of regular expressions
    to match column names, and a flag to indicate if you want to select
    or deselect those columns.

    """

    def __init__(
        self,
        col_select: Optional[List[str]] = None,
        select_not_deselect: bool = True,
        inplace: bool = False,
        **kwargs: Any
    ):
        """Construct transformer.

        Parameters
        ----------
        col_select : list of str  (default: [])
            list of regular expression strings

        select_not_deselect : bool (default: True)
            if True, select columns matching any expressions in col_select
            if False, deselect columns matching any expressions in col_select

        inplace : bool (default: False)
            whether .transform is applied inplace

        **kwargs :
            Additional unused arguments are mopped up.

        """
        if col_select is None:
            col_select = []

        self.col_select = col_select
        self._col_select_regexs = [
            re.compile(str(exp)) for exp in list(self.col_select)
        ]

        self._select_not_deselect = select_not_deselect
        self._inplace = bool(inplace)

    @property
    def inplace(self) -> bool:
        """Get the in place property."""
        # This trivial get is to support backwards compatibility with 20.1
        # column selection transformer property naming conventions
        return self._inplace

    @inplace.setter
    def inplace(self, value: bool) -> None:
        """Get the in place property."""
        # This trivial set is to support backwards compatibility with 20.1
        # column selection transformer property naming conventions
        self._inplace = value

    @property
    def select_not_deselect(self) -> bool:
        """Get the select not deselect property."""
        # This trivial get is to support backwards compatibility with 20.1
        # column selection transformer property naming conventions
        return self._select_not_deselect

    @select_not_deselect.setter
    def select_not_deselect(self, value: bool) -> None:
        """Set the select not deselect property."""
        # This trivial set is to support backwards compatibility with 20.1
        # column selection transformer property naming conventions
        self._select_not_deselect = value

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

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data, (de)selecting columns based on regex.

        Parameters
        ----------
        X : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        Returns
        -------
        pandas.DataFrame with only matching columns selected

        """
        inplace = self.inplace
        # Identify columns to select/deselect
        col_select = [list(filter(r.match, list(X))) for r in self._col_select_regexs]
        # Flatten the array
        col_select = [item for row in col_select for item in row]
        if self.select_not_deselect:
            result = X.drop(X.columns.difference(col_select), 1, inplace=inplace)
        else:
            result = X.drop(col_select, 1, inplace=inplace)
        if not inplace:
            X = result
        return X
