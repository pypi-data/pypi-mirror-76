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
"""Impute method transformer."""
from typing import Any

from ayx_learn.utils.constants import SimpleStringNamespace
from ayx_learn.utils.exceptions import ImputationError
from ayx_learn.utils.validate import validate_enum

import numpy as np

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


def mean(series: pd.Series, *args):  # type: ignore  # type: ignore
    """Calculate fill value in MEAN mode."""
    return series.mean()


def mode(series: pd.Series, *args):  # type: ignore  # type: ignore
    """Calculate fill value in MODE mode."""
    mode_as_series = series.mode()
    return mode_as_series[0] if len(mode_as_series) > 0 else np.nan


def median(series: pd.Series, *args):  # type: ignore  # type: ignore
    """Calculate fill value in MEDIAN mode."""
    return series.median()


def value(_, val, *args):  # type: ignore
    """Calculate fill value in VALUE mode."""
    return val


def custom(series: pd.Series, _, func, *args):  # type: ignore  # type: ignore
    """Calculate fill value in CUSTOM mode."""
    if not func:
        raise ValueError("Function has not been properly specified.")
    return func(series)


impute_method_dict = {
    "MEAN": mean,
    "MEDIAN": median,
    "MODE": mode,
    "VALUE": value,
    "CUSTOM": custom,
}

# Auto generate the Enum for Impute methods based on the above dict.
# This implicitly forces any additional imputation methods to have
# associated functions
ImputeMethods = SimpleStringNamespace(*list(impute_method_dict.keys()))


class ImputeTransformer(TransformerMixin, BaseEstimator):
    """Transformer for imputing missing values in column(s)."""

    def __init__(  # type: ignore
        self,
        method: ImputeMethods = ImputeMethods.MEAN,  # type: ignore
        value: Any = 0.0,
        custom_method=None,
        colname=None,
        inplace=False,
        **kwargs,
    ):
        """Construct transformer.

        Parameters
        ----------
        method : str
            If "MEAN", impute with mean of column.
            If "MEDIAN", impute with median of column.
            If "MODE", impute with mode of column.
            If "VALUE", impute with parameter `value`.
            If "CUSTOM", impute with result of parameter `custom_method` applied to column.

        value :
            Scalar, appropriate type for given column(s).
            Only used when `method` is "VALUE".

        custom_method :
            Callable, applied to column to determine constant imputation value.
            Only used when `method` is "CUSTOM".

        colname : str, optional
            If specified, only perform imputation on specified column.

        inplace : bool (default: False)
            Whether .transform is applied in-place.

        **kwargs
            Additional arguments to mop up.

        """
        self.method = method
        self.value = value
        self.col_value_dict = {}  # type: ignore
        if custom_method:
            self.custom_method = custom_method
        else:
            self.__custom_method = None
        self.colname = colname
        self._inplace = bool(inplace)

    @property
    def method(self):  # type: ignore
        """Get imputation method."""
        return self.__method

    @method.setter
    def method(self, method: str) -> None:
        """Set imputation method."""
        validate_enum(method, ImputeMethods)
        self.__method = method

    @property
    def value(self):  # type: ignore
        """Get value in VALUE imputation method."""
        return self.__value

    @value.setter
    def value(self, value: float):  # type: ignore
        """Set value in VALUE imputation method."""
        self.__value = value

    @property
    def custom_method(self):  # type: ignore
        """Getter for custom_method used in the CUSTOM imputer mode."""
        return self.__custom_method

    @custom_method.setter
    def custom_method(self, custom_method):  # type: ignore
        """Setter for custom_method used in the CUSTOM imputer mode."""
        if not callable(custom_method):
            raise ValueError("Custom method must be callable.")
        self.__custom_method = custom_method

    def transform(  # type: ignore
        self, x: pd.DataFrame, y=None, **kwargs
    ) -> pd.DataFrame:
        """Impute the colnames in the DataFrame.

        Parameters
        ----------
        x : pandas.DataFrame, shape = (n_features, n_observations)
            Data to transform.

        **kwargs
            Additional arguments to mop up.

        Returns
        -------
        pandas.DataFrame, shape = (n_features, n_observations)
            Imputed DataFrame

        Raises
        ------
        ValueError
            - If imputation method is invalid.
            - If column present that wasn't used in `fit`.

        """
        columns_to_impute = x.columns
        if self.colname is not None:
            columns_to_impute = [self.colname]
        inplace = self._inplace
        if not inplace:
            x = x.copy()
        for column in columns_to_impute:
            try:
                # Extract the column
                data = x[column]

                # Calculate the fill value
                try:
                    value = self.col_value_dict[column]
                except KeyError:
                    raise ValueError("A column is present that was not during fit.")

                # Perform imputation
                if data.dtype.name == "category" and value not in data.cat.categories:
                    data = data.cat.add_categories(value)
                x.loc[:, column] = data.fillna(value)
            except Exception as err:
                raise err
        return x

    def fit(self, x: pd.DataFrame, y=None, **kwargs):  # type: ignore  # type: ignore
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
        method = self.method
        columns_to_impute = x.columns
        if self.colname is not None:
            columns_to_impute = [self.colname]
        for column in columns_to_impute:
            try:
                # Extract the column
                data = x[column]

                # Calculate the fill value
                value = impute_method_dict[method](  # type: ignore
                    data, self.value, self.custom_method
                )

                try:
                    if not np.isfinite(value):
                        raise ImputationError(  # type: ignore
                            f"Imputation of {value} for {column} is not finite.", column
                        )
                except TypeError:
                    pass

                # Save it
                self.col_value_dict[column] = value

            except Exception as err:
                raise err
        return self
