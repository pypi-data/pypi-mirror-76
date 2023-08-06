# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Accuracy measure supporting aggregation over multiple folds."""
import logging

from ayx_learn.evaluations.classification import ClassificationEvaluation
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.metrics import roc_curve


logger = logging.getLogger(__name__)


class ROC(ClassificationEvaluation, MultiFoldEvaluation):
    """ROC curve support with fold-independent processing.

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

    interpolator (Optional) : function
        Interpolator to use for estimating value at unprovided x points
        Defaults to np.interp (linear interpolation).

    x_points (Optional) : int (> 2) or array-like; Default: 100
        If array-like, all values in [0, 1] to be used as x points for ROC curve
        If int, must be > 2; x points for ROC curve will be equally-spaced in [0, 1]
        Will default to 100 (i.e. x points of [0, .01, .02, ..., .99, 1])

    """

    # empty chart for when ROC is not well-defined
    _empty_chart = {"fpr": [], "tpr": []}  # type: ignore

    def __init__(  # type: ignore
        self,
        levels,
        encoded_levels=None,
        positive_class=None,
        interpolator=None,
        x_points=None,
    ):
        """Construct the evaluation."""
        ClassificationEvaluation.__init__(  # type: ignore
            self, levels, encoded_levels, positive_class
        )
        MultiFoldEvaluation.__init__(self)  # type: ignore

        if x_points is None:
            self._x_points = np.linspace(0, 1, num=101)
        elif isinstance(x_points, int):
            self._x_points = np.linspace(0, 1, num=x_points)
        else:
            self._x_points = x_points

        if interpolator is None:
            self._interpolator = np.interp
        else:
            self._interpolator = interpolator

        if positive_class is None:
            self._positive_class = levels[0]
        else:
            level_type = type(levels[0])
            self._positive_class = level_type(positive_class)
        self._positive_class_index = levels.index(self._positive_class)
        self._positive_class_encoding = self._encoded_levels[self._positive_class_index]

    def evaluate(  # type: ignore
        self, y_true, y_pred_proba, model_level_encodings, **kwargs
    ):
        """Run the evaluation."""
        if self._positive_class_encoding not in model_level_encodings:
            logger.warning(
                "Positive class not present in data. ROC chart is not well-defined"
            )
            return self._empty_chart

        idx = list(model_level_encodings).index(self._positive_class_encoding)
        fpr, tpr, _ = roc_curve(
            y_true, y_pred_proba[:, idx], pos_label=self._positive_class_encoding
        )
        # Force y[0] to be 0 for expectation consistency
        # Done properly, this would use the inverse of the aggregator, but that's not currently feasible
        xs = self._x_points
        ys = self._interpolator(self._x_points, fpr, tpr)
        ys[0] = 0.0
        return {"fpr": xs, "tpr": ys}

    def format(self, roc):  # type: ignore
        """Run the format to external representation."""
        return {"xs": roc["fpr"], "ys": roc["tpr"]}

    def inverse_format(self, formatted_score):  # type: ignore
        """Run the inverse format to internal representation."""
        return {"fpr": formatted_score["xs"], "tpr": formatted_score["ys"]}

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        try:
            return {
                "fpr": self._scores[0]["fpr"],  # xs same across folds
                "tpr": np.mean([score["tpr"] for score in self.scores], axis=0),
            }
        except Exception as error:
            logger.exception(error)
            return self._empty_chart
