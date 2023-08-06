# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements abstract class for evaluations on classification data."""
import abc

from ayx_learn.evaluations.evaluation import Evaluation


class ClassificationEvaluation(Evaluation):
    """Abstract class for evaluations for classification models.

    Parameters
    ----------
    levels : array-like
        Collection of distinct values that appear in target

    encoded_levels (Optional) : array-like
        Numeric values corresponding to those in `levels`.
        Must have same length as `levels`.
        If not provided, assumed to be the same as `levels`.

    positive_class (Optional) : scalar
        If provided, should be an element of `levels` corresponding to class of interest

    """

    def __init__(  # type: ignore
        self, levels, encoded_levels=None, positive_class=None
    ):
        """Construct the evaluation."""
        Evaluation.__init__(self)  # type: ignore
        self._levels = list(levels)
        self._encoded_levels = (
            self._levels if encoded_levels is None else list(encoded_levels)
        )
        assert len(self._levels) == len(self._encoded_levels)
        if positive_class is not None:
            assert positive_class in levels
        self._positive_class = positive_class

    @abc.abstractmethod
    def evaluate(  # type: ignore
        self, y_true, y_pred, y_pred_proba, model_level_encodings=None
    ):
        """Abstract method for evaluating new data.

        Parameters
        ----------
        y_true : array, shape = [n_samples]
            True labels

        y_pred : array, shape = [n_samples]
            Estimated targets as returned by a classifier.

        y_pred_proba : array, shape = [n_samples, n_classes]
            Target score probabilities, one for each level in `model_level_encodings`

        model_level_encodings (Optional) : array
            Unique values classifier was trained on. All should be present in `encoded_levels`.
            If not provided, assumed to all in be `encoded_levels`

        """

    @property
    def levels(self):  # type: ignore
        """List of distinct values that appear in target data."""
        return self._levels

    @property
    def encoded_levels(self):  # type: ignore
        """List of distinct values that appear in target data after encoding."""
        return self._encoded_levels

    @property
    def positive_class(self):  # type: ignore
        """Positive class (may be None) for data."""
        return self._positive_class
