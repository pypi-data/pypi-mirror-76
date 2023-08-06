# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Accuracy measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.classification import ClassificationEvaluation
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.metrics import accuracy_score


class Accuracy(ClassificationEvaluation, MultiFoldEvaluation):
    """Accuracy measure supporting fold-independent evaluation and aggregation across folds.

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

    """

    def __init__(  # type: ignore
        self, levels, encoded_levels=None, positive_class=None
    ):
        """Construct the evaluation."""
        ClassificationEvaluation.__init__(  # type: ignore
            self, levels, encoded_levels, positive_class
        )
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, y_true, y_pred, **kwargs):  # type: ignore
        """Run the evaluation."""
        return accuracy_score(y_true, y_pred)

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return np.mean(self.scores)
