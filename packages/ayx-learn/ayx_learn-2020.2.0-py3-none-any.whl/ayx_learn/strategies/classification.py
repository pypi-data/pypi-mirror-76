# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements base abstract strategy for classification analyses."""
from typing import Any, Dict, Tuple, Type

from ayx_learn.base import BaseInspector, Pipeline
from ayx_learn.inspectors import (
    ClassificationImportanceInspector,
    DataFrameNullsInspector,
    DataFrameTypeInspector,
)
from ayx_learn.strategies.supervised import SupervisedStrategy
from ayx_learn.typing import ArrayLike, SupportsTransform

import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_array


def get_rarest_class(values: ArrayLike, dropna: bool = True) -> Any:
    """Get rarest class in a column.

    Parameters
    ----------
    values : ArrayLike

    dropna : bool
        drop null values (i.e. exclude the possibility that null is rarest)

    """
    series = pd.Series(check_array(values))
    if dropna:
        series = series.dropna()
    levels_by_frequency = {}  # type: ignore
    for value in list(series):
        levels_by_frequency[value] = levels_by_frequency.get(value, 0) + 1
    return min(levels_by_frequency, key=levels_by_frequency.get)


class ClassificationStrategy(SupervisedStrategy):
    """Base strategy for classification analyses."""

    n_splits = 3
    splitter_rng = 42

    @property
    def partitioner(self):  # type: ignore
        """Get the partitioner."""
        return StratifiedKFold(
            n_splits=self.n_splits, shuffle=True, random_state=self.splitter_rng
        )

    @property
    def y_encoder(self) -> SupportsTransform:
        """Get the encoder for the target variable.

        Returns
        -------
        Transformer

        """
        return LabelEncoder()  # type: ignore  # not sure why mypy doesn't resolve type

    def get_prediction_details(  # type: ignore  # mypy doesn't like adding `all_data`
        self,
        pipeline: Pipeline,
        test_data: Tuple[pd.DataFrame, pd.Series],
        all_data: Tuple[pd.DataFrame, pd.Series],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get prediction details of pipeline.

        Parameters
        ----------
        pipeline : Pipeline

        test_data : Tuple[ArrayLike]
            X, y data held out from traiing

        all_data : Tuple[ArrayLike]
            X, y train + test data

        **kwargs : mop-up

        Returns
        -------
        dict of str names to values

        """
        X_test, y_test = test_data
        y_pred, y_pred_proba = pipeline.predict_with_proba(X_test)
        _, all_y = all_data
        positive_class = get_rarest_class(all_y)
        levels = list(all_y.unique())
        encoded_levels = list(self.y_encoder.fit_transform(levels))
        model_level_encodings = pipeline.estimator.classes_  # type: ignore
        return {
            # model predictions of data; same length as `test_data`
            "y_pred": y_pred,
            # model prediction probabilities of data
            # y_pred_proba[i, j] is the probability of model_level_encodings[j]
            # for record test_data[i]
            "y_pred_proba": y_pred_proba,
            "levels": levels,
            "encoded_levels": encoded_levels,
            # the levels (subset of `encoded_levels`) present during model training
            "model_level_encodings": model_level_encodings,
            # the class of interest (may be None)
            "positive_class": positive_class,
            # the actual target values for the test data
            "y_true": y_test,
            "pipeline": pipeline,
            # the predictor test data
            "x_test": X_test,
        }

    @property
    def steps(self) -> Dict[str, Type[BaseInspector]]:
        """Get the inspectors for a given problem type.

        Returns
        -------
        Dictionary mapping PipelineStep type to an Inspector / Transformer

        """
        return {
            "COLUMN_TYPING": DataFrameTypeInspector,
            "NA_HANDLING": DataFrameNullsInspector,
            "FEATURE_IMPORTANCE": ClassificationImportanceInspector,
        }
