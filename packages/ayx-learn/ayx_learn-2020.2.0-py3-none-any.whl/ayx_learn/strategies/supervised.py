# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements base supervised strategy."""
import abc
from typing import Tuple

from ayx_learn.base import Strategy
from ayx_learn.transformers import IdentityTransformer
from ayx_learn.typing import SupportsTransform

import numpy as np

import pandas as pd


class SupervisedStrategy(Strategy):
    """Strategy for problems with a target variable."""

    def __init__(self, target: str):
        """Construct the strategy.

        Parameters
        ----------
        target : str
            name of target

        """
        self.target = target

    def get_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Given a dataframe, separate the predictor and target data.

        Parameters
        ----------
        df : pandas DataFrame

        Returns
        -------
        X : pandas DataFrame

        y : 1-dim numpy array

        """
        x_names = [name for name in list(df) if name != self.target]
        X = df[x_names]
        y = df[self.target]
        return X, y

    @property
    def y_encoder(self) -> SupportsTransform:
        """Get the encoder for the target variable.

        Returns
        -------
        sklearn TransformerMixin

        """
        return IdentityTransformer()

    @property
    @abc.abstractmethod
    def partitioner(self):  # type: ignore
        """Paritioner for cross validation."""
        pass

    def get_partition(  # type: ignore
        self, fold_idx: int, X: pd.DataFrame, y: pd.Series
    ) -> Tuple[Tuple[pd.DataFrame, pd.Series], Tuple[pd.DataFrame, pd.Series]]:
        """Given data, get a partition of it.

        Parameters
        ----------
        fold_idx : int
            index of partition

        X : array-like, shape (n_observations, n_features)

        y : array-like, shape (n_observations)

        """
        splits = list(self.partitioner.split(X, y))
        train_idx, test_idx = splits[fold_idx]
        X_train = X.loc[train_idx, :]
        X_test = X.loc[test_idx, :]
        y = self.y_encoder.fit_transform(y)
        y_train = y[train_idx]
        y_test = y[test_idx]
        # Use of drop=True is required in a certain edge case -
        # namely when the dataset already contains columns named 'index' and 'level_0'
        X_train.reset_index(drop=True, inplace=True)
        X_test.reset_index(drop=True, inplace=True)
        train_data = (X_train, y_train)
        test_data = (X_test, y_test)
        return train_data, test_data

    def validate_target(self, target: np.array) -> None:
        """Validate that the target column is acceptable for the strategy."""

    def validate_df(self, df: pd.DataFrame) -> None:
        """Validate that object is a dataframe that contains the expected target."""
        assert isinstance(df, pd.DataFrame), "df argument must be pandas.DataFrame"
        assert self.target in df, "target missing from df"
        self.validate_target(df[self.target])
