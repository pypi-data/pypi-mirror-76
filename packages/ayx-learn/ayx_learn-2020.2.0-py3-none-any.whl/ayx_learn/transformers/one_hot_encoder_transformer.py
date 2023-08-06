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
"""One hot encoder implementation.

TODO: Use typing_extensions.Literal to clean up type hints.
TODO: Fix incorrect typehint on categories; should be a list of lists of scalars
TODO: categorical_features deprecated; will be removed in 0.22

"""
import logging
from typing import Any, Dict, List, Optional, Set, TypeVar, Union

from ayx_learn.utils.exceptions import OheUnexpectedLevelsException
from ayx_learn.utils.validate import validate_no_nulls

import numpy as np

import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.utils.validation import check_is_fitted

logger = logging.getLogger(__name__)


T = TypeVar("T", bound="OneHotEncoderTransformer")


class OneHotEncoderTransformer(OneHotEncoder):
    """Wrapper around sklearn OneHotEncoder with consistent support for column names."""

    def __init__(
        self,
        categorical_columns: Optional[Union[str, List[str]]] = "auto",
        categorical_features: Optional[Union[str, List[int], List[bool]]] = None,
        categories: Optional[Union[List[str], List[int]]] = None,
        handle_unknown: str = "error",
    ):
        """Construct transformer.

        Parameters
        ----------
        categorical_columns : list of column names, "auto" or None
            If list of column names, columns to encode.
            If "auto", encode any columns with type 'object' or 'category'.
            If None, encode all columns.

        categorical_features: see documentation for sklearn OneHotEncoder [1]

        categories: see documentation for sklearn OneHotEncoder [1]

        handle_unknown : see documentation for sklearn OneHotEncoder [1]

        [1] : https://scikit-learn.org/0.21/modules/generated/sklearn.preprocessing.OneHotEncoder.html

        """
        super().__init__(
            categorical_features=categorical_features,
            categories=categories,
            sparse=False,
            dtype=np.float64,
            handle_unknown=handle_unknown,
        )
        self.categorical_columns = categorical_columns
        self._input_columns = []  # type: Union[str, List[str]]
        self._columns_to_encode = []  # type: Union[str, List[str]]

    @property
    def categorical_columns(self) -> Optional[Union[str, List[str]]]:
        """Getter for categorical columns."""
        return self.__categorical_columns

    @categorical_columns.setter
    def categorical_columns(self, value: Optional[Union[str, List[str]]]) -> None:
        if not isinstance(value, list) and value != "auto" and value is not None:
            raise ValueError(
                "categorical_columns must be a list of column names, 'auto', or None."
            )
        self.__categorical_columns = value

    def fit(self: T, X: pd.DataFrame, *_: Any, **__: Any) -> T:
        """Fit transformer.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Fitting dependent data

        *_, **__ :
            Additional arguments to mop up

        Returns
        -------
        self

        """
        self._input_columns = list(X)

        if self.categorical_columns is None:
            self._columns_to_encode = self._input_columns
        elif self.categorical_columns == "auto":
            self._columns_to_encode = X.select_dtypes(
                include=["category", "object"]
            ).columns.tolist()
        else:
            # TODO: clean typehints when on python 3.8
            self._columns_to_encode = self.categorical_columns

        self.categories = [
            sorted(list(set(X[col].values))) for col in self._columns_to_encode
        ]

        try:
            super().fit(X[self._columns_to_encode])
        except ValueError as e:
            logger.exception(e)
            validate_no_nulls(X)
            raise e

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data.

        Parameters
        ----------
        X : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        Returns
        -------
        pandas.DataFrame with new columns.

        """
        check_is_fitted(self, ["categories_"])

        if set(X.columns) != set(self._input_columns):
            err_str = (
                f"Incoming columns don't match fitted columns: {self._input_columns}"
            )
            logger.error(err_str)
            raise ValueError(err_str)
        elif list(X.columns) != list(self._input_columns):
            X = X[self._input_columns]

        try:
            X_encoded = super().transform(X[self._columns_to_encode])  # noqa: N806
        except ValueError as e:
            logger.exception(e)
            validate_no_nulls(X)
            self._validate_no_unexpected_categories(X)
            raise e

        X_encoded = pd.DataFrame(  # noqa: N806
            X_encoded, columns=self.get_categorical_feature_names(), index=X.index
        )

        unencoded_columns = [
            col for col in list(X) if col not in self._columns_to_encode
        ]

        if len(unencoded_columns) == 0:
            return X_encoded

        unencoded_df = X[unencoded_columns]

        X_encoded[list(unencoded_df)] = unencoded_df

        return X_encoded

    def get_feature_names_(self) -> List[str]:
        """Get the the names of all the output features."""
        check_is_fitted(self, ["categories_"])

        features = self.get_categorical_feature_names()

        unique_names = set(self._input_columns)
        for idx, feature in enumerate(features):
            new_feature = self._get_unique_name(feature, unique_names)
            features[idx] = new_feature
            unique_names.add(new_feature)

        for feature in self._input_columns:
            if feature not in self._columns_to_encode:
                features.append(feature)

        return features

    def get_categorical_feature_names(self) -> List[str]:
        """Get the names of the output categorical features."""
        obj = super().get_feature_names(self._columns_to_encode).tolist()
        return obj  # type: ignore

    def get_link(self) -> Dict[str, str]:
        """Get the link between original column names and encoded ones.

        Returns
        -------
        Dict
            keys are feature names after encoding
            values are the feature names before encoding that they originate from.

        """
        original_features = self._columns_to_encode
        encoded_features = self.get_feature_names_()

        num_features = [len(x) for x in self.categories_]
        num_features.insert(0, 0)

        category_idxs = np.cumsum(num_features).tolist()
        category_idxs = [
            (category_idxs[i], category_idxs[i + 1])
            for i in range(len(category_idxs) - 1)
        ]

        link = {
            col: col
            for col in self._input_columns
            if col not in self._columns_to_encode
        }
        for original_feature_idx, (encoded_start, encoded_end) in enumerate(
            category_idxs
        ):
            for encoded_feature_idx in range(encoded_start, encoded_end):
                link[encoded_features[encoded_feature_idx]] = original_features[
                    original_feature_idx
                ]

        return link

    @staticmethod
    def _get_unique_name(name: str, set_: Set[str]) -> str:
        if name not in set_:
            return name

        idx = 2
        while True:
            new_name = f"{name}_{idx}"
            if new_name not in set_:
                return new_name

            idx += 1

    def _validate_no_unexpected_categories(self, X: pd.DataFrame) -> None:
        for idx, col in enumerate(self._columns_to_encode):
            expected_cats = set(self.categories_[idx])
            actual_cats = set(X[col].unique())

            if not actual_cats.issubset(expected_cats):
                unexpected_cats = actual_cats.difference(expected_cats)
                err_str = (
                    f"Found unexpected categories {unexpected_cats} in column {col}."
                )
                logger.error(err_str)
                raise OheUnexpectedLevelsException(  # type: ignore
                    err_str, (unexpected_cats, col)
                )

    def fit_transform(self, X: pd.DataFrame, *_: Any, **__: Any) -> pd.DataFrame:
        """Fit, then transform data.

        Parameters
        ----------
        X : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        *_, **__ :
            Additional arguments to mop up

        Returns
        -------
        pandas.DataFrame

        """
        self.fit(X)
        return self.transform(X)
