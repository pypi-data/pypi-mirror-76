# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Multiclass analogue of AUC metric.

Specifically, averages across AUC estimations for all class-class comparisons.
"""
import logging

from ayx_learn.evaluations.base_auc import BaseAUC
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


logger = logging.getLogger(__name__)


class M(BaseAUC):
    """M metric.

    A macro-averaged analogue of AUC for multiclass problems [1]_ .
    Supports fold-independent scoring and aggregation.

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
        If not provided, assumed to be first of `levels`

    References
    ----------
    .. [1] Hand and Till. A Simple Generalisation of the Area Under the ROC Curve for Multiple Class Classification Problems.

    """

    def evaluate(self, y_true, y_pred_proba, **kwargs):  # type: ignore
        """Run the evaluation."""
        # TODO: handle the case where there are missing levels
        try:
            return m_auc(y_true, y_pred_proba)
        except Exception as error:
            logger.warning(error)
            return None

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        try:
            return np.mean(scores)
        except Exception as error:
            logger.warning(error)
            return None


def a_metric(
    positive_class_proba: np.ndarray, negative_class_proba: np.ndarray
) -> float:  # class_0 / class_1 instead of positive_class and negative_class
    """AUC approximation.

    Parameters
    ----------
    positive_class_proba : array, shape = [i_samples]
        Prediction probabilities for the positive class for records with actual label of the positive class

    negative_class_proba : array, shape = [j_samples]
        Prediction probabilities for the positive class for records with actual label of the comparison class

    Returns
    -------
    float
        AUC approximation, per [1]_

    References
    ----------
    .. [1] Hand and Till. A Simple Generalisation of the Area Under the ROC Curve for Multiple Class Classification Problems. Equation 3.

    """
    if not (
        isinstance(positive_class_proba, np.ndarray)
        and isinstance(negative_class_proba, np.ndarray)
        and len(positive_class_proba.shape) == len(negative_class_proba.shape) == 1
    ):
        raise TypeError(
            "positive_class_proba and negative_class_proba must be 1 dimensional numpy arrays"
        )

    if positive_class_proba.size == 0 or negative_class_proba.size == 0:
        raise ValueError(
            "positive_class_proba and negative_class_proba must be non-empty"
        )

    n0 = positive_class_proba.size
    n1 = negative_class_proba.size
    # Efficient sorting while leaving everything in numpy
    # Doing this the obvious way with loops is much slower
    probas = np.concatenate((positive_class_proba, negative_class_proba))

    # other options that break ties by averaging / randomizing are slower
    temp = probas.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(start=1, stop=len(probas) + 1)

    s0 = sum(ranks[:n0])

    return (s0 - n0 * (n0 + 1) / 2) / (n0 * n1)  # type: ignore


def m_auc(y_true: np.ndarray, y_pred_proba: np.ndarray) -> float:
    """Multiclass AUC approximation, a macro-averaging of `a_metric`.

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        Encoded values of actual labels. Should all be in `range(n_classes)`

    y_pred_proba : array, shape = [n_samples, n_classes]
        Prediction probabilities for all classes

    Returns
    -------
    float
        AUC approximation, per [1]_

    References
    ----------
    .. [1] Hand and Till. A Simple Generalisation of the Area Under the ROC Curve for Multiple Class Classification Problems. Equation 7.

    """
    if not (isinstance(y_pred_proba, np.ndarray) and isinstance(y_true, np.ndarray)):
        raise TypeError("y_pred_proba and y_true must be numpy ndarrays")
    if y_pred_proba.shape[0] != y_true.size:
        raise ValueError(
            "y_pred_proba should have shape [n_samples, n_classes] and y_true should have shape [n_samples]. n_samples inconsistent"
        )
    if y_pred_proba.shape[1] < 2:
        raise ValueError(
            "y_pred_proba should have shape [n_samples, n_classes]. n_classes must be >= 2"
        )

    n_classes = y_pred_proba.shape[1]
    a_metrics_scores = []
    for j in range(n_classes):
        # relevant row indices are by actual label
        j_indices = np.where(y_true == j)[0]
        for i in range(j):
            i_indices = np.where(y_true == i)[0]
            j_score = a_metric(
                positive_class_proba=y_pred_proba[j_indices, j],
                negative_class_proba=y_pred_proba[i_indices, j],
            )
            i_score = a_metric(
                positive_class_proba=y_pred_proba[i_indices, i],
                negative_class_proba=y_pred_proba[j_indices, i],
            )
            a_metrics_scores.append((j_score + i_score) / 2)
    return (  # type: ignore
        2 * sum(a_metrics_scores) / (n_classes * (n_classes - 1))  # type: ignore
    )
